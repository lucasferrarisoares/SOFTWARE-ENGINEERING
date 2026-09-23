import argparse
import threading
from socketserver import ThreadingMixIn
from xmlrpc.client import Fault
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from rpc_utils import criar_proxy


ENDERECO_PADRAO = "127.0.0.1"
PORTA_PADRAO = 8000
PORTA_BASE_SERVIDORES = 9000
NUM_SERVIDORES = 3
METODOS_PERMITIDOS = {"encurtar", "resolver"}

_contexto_requisicao = threading.local()


class ManipuladorRPC(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/", "/RPC2")

    def do_POST(self):
        endereco_encaminhado = self.headers.get("X-Forwarded-For")
        if endereco_encaminhado:
            endereco_cliente = endereco_encaminhado.split(",", 1)[0].strip()
        else:
            host, porta = self.client_address[:2]
            endereco_cliente = f"{host}:{porta}"
        _contexto_requisicao.endereco_cliente = endereco_cliente
        try:
            super().do_POST()
        finally:
            if hasattr(_contexto_requisicao, "endereco_cliente"):
                del _contexto_requisicao.endereco_cliente


class ServidorXMLRPCConcorrente(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True
    allow_reuse_address = True


class Balanceador:
    def __init__(self, servidores, timeout):
        self.servidores = servidores
        self.timeout = timeout
        self._indice = 0
        self._lock_indice = threading.Lock()

    def ping(self):
        disponibilidade = []
        for servidor in self.servidores:
            try:
                with criar_proxy(servidor["url"], self.timeout) as proxy:
                    resposta = proxy.ping()
                disponivel = resposta.get("status") == "ok"
            except Exception:
                disponivel = False
            disponibilidade.append(
                {"servidor_id": servidor["id"], "disponivel": disponivel}
            )
        return {"status": "ok", "servidores": disponibilidade}

    def _selecionar_servidor(self):
        with self._lock_indice:
            indice_inicial = self._indice
            self._indice = (self._indice + 1) % len(self.servidores)
        return indice_inicial

    def _dispatch(self, metodo, parametros):
        if metodo not in METODOS_PERMITIDOS:
            raise Fault(404, f"Método RPC desconhecido: {metodo}")
        if len(parametros) != 1:
            raise Fault(400, f"O método {metodo} exige exatamente um argumento.")

        indice_inicial = self._selecionar_servidor()
        endereco_cliente = getattr(
            _contexto_requisicao, "endereco_cliente", "desconhecido"
        )
        erros = []

        for deslocamento in range(len(self.servidores)):
            indice = (indice_inicial + deslocamento) % len(self.servidores)
            servidor = self.servidores[indice]
            print(
                f"[BALANCEADOR] Encaminhando {metodo}() para Servidor "
                f"{servidor['id']} ({servidor['url']})",
                flush=True,
            )
            try:
                with criar_proxy(servidor["url"], self.timeout) as proxy:
                    funcao_remota = getattr(proxy, metodo)
                    resultado = funcao_remota(*parametros, endereco_cliente)
                print(
                    f"[BALANCEADOR] Resposta recebida do Servidor "
                    f"{servidor['id']}",
                    flush=True,
                )
                return resultado
            except Exception as erro:
                erros.append(f"Servidor {servidor['id']}: {erro}")
                print(
                    f"[BALANCEADOR] Servidor {servidor['id']} indisponível; "
                    "tentando o próximo.",
                    flush=True,
                )

        return {
            "status": "erro",
            "mensagem": "Nenhum servidor RPC está disponível.",
            "detalhes": erros,
        }


def criar_parser():
    parser = argparse.ArgumentParser(description="Balanceador Round-Robin XML-RPC")
    parser.add_argument("--host", default=ENDERECO_PADRAO)
    parser.add_argument("--porta", type=int, default=PORTA_PADRAO)
    parser.add_argument("--host-servidores", default=ENDERECO_PADRAO)
    parser.add_argument("--porta-base-servidores", type=int, default=PORTA_BASE_SERVIDORES)
    parser.add_argument("--timeout", type=float, default=5.0)
    return parser


def main():
    argumentos = criar_parser().parse_args()
    servidores = [
        {
            "id": servidor_id,
            "url": (
                f"http://{argumentos.host_servidores}:"
                f"{argumentos.porta_base_servidores + servidor_id}"
            ),
        }
        for servidor_id in range(NUM_SERVIDORES)
    ]
    balanceador = Balanceador(servidores, argumentos.timeout)

    for estado in balanceador.ping()["servidores"]:
        texto = "disponível" if estado["disponivel"] else "indisponível"
        print(
            f"[BALANCEADOR] Servidor {estado['servidor_id']}: {texto}", flush=True
        )

    with ServidorXMLRPCConcorrente(
        (argumentos.host, argumentos.porta),
        requestHandler=ManipuladorRPC,
        allow_none=True,
        logRequests=False,
    ) as servidor_rpc:
        servidor_rpc.register_function(balanceador.ping, "ping")
        servidor_rpc.register_instance(balanceador)

        print(
            f"[BALANCEADOR] Iniciado em {argumentos.host}:{argumentos.porta}",
            flush=True,
        )
        print(
            f"[BALANCEADOR] Estratégia: Round-Robin com {NUM_SERVIDORES} servidores",
            flush=True,
        )
        print("[BALANCEADOR] Aguardando requisições...", flush=True)
        servidor_rpc.serve_forever()


if __name__ == "__main__":
    main()
