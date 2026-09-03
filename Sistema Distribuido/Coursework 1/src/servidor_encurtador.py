import argparse
import secrets
import sqlite3
import string
import threading
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


ENDERECO_PADRAO = "127.0.0.1"
PORTA_BASE_PADRAO = 9000
NUM_SERVIDORES = 3
PREFIXO_URL = "sddin.uem/"
CARACTERES_CODIGO = string.ascii_letters + string.digits
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
BANCO_PADRAO = RAIZ_PROJETO / "data" / "urls.db"

_contexto_requisicao = threading.local()


class ManipuladorRPC(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/", "/RPC2")

    def do_POST(self):
        host, porta = self.client_address[:2]
        _contexto_requisicao.endereco = f"{host}:{porta}"
        try:
            super().do_POST()
        finally:
            if hasattr(_contexto_requisicao, "endereco"):
                del _contexto_requisicao.endereco


class ServidorXMLRPCConcorrente(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True
    allow_reuse_address = True


class RepositorioURLs:
    def __init__(self, caminho_banco):
        self.caminho_banco = Path(caminho_banco).resolve()
        self.caminho_banco.parent.mkdir(parents=True, exist_ok=True)
        self._inicializar()

    def _conectar(self):
        conexao = sqlite3.connect(self.caminho_banco, timeout=15)
        conexao.execute("PRAGMA busy_timeout = 15000")
        return conexao

    def _inicializar(self):
        with self._conectar() as conexao:
            conexao.execute("PRAGMA journal_mode = WAL")
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    url_original TEXT PRIMARY KEY,
                    codigo TEXT NOT NULL UNIQUE
                )
                """
            )

    def buscar_por_url(self, url):
        with self._conectar() as conexao:
            linha = conexao.execute(
                "SELECT codigo FROM urls WHERE url_original = ?", (url,)
            ).fetchone()
        return linha[0] if linha else None

    def buscar_por_codigo(self, codigo):
        with self._conectar() as conexao:
            linha = conexao.execute(
                "SELECT url_original FROM urls WHERE codigo = ?", (codigo,)
            ).fetchone()
        return linha[0] if linha else None

    def inserir(self, url, codigo):
        conexao = self._conectar()
        try:
            conexao.execute(
                "INSERT INTO urls (url_original, codigo) VALUES (?, ?)",
                (url, codigo),
            )
            conexao.commit()
            return True
        except sqlite3.IntegrityError:
            conexao.rollback()
            return False
        finally:
            conexao.close()


class ServicoEncurtador:
    def __init__(self, servidor_id, repositorio):
        self.servidor_id = servidor_id
        self.repositorio = repositorio

    def _registrar_requisicao(self, operacao, endereco_cliente=None):
        endereco = endereco_cliente or getattr(
            _contexto_requisicao, "endereco", "desconhecido"
        )
        print(
            f"[SERVIDOR {self.servidor_id}] Requisição recebida: {operacao}",
            flush=True,
        )
        print(f"[SERVIDOR {self.servidor_id}] Cliente: {endereco}", flush=True)

    def _resposta(self, **campos):
        return {"servidor_id": self.servidor_id, **campos}

    def ping(self):
        return self._resposta(status="ok")

    def encurtar(self, url, endereco_cliente=None):
        self._registrar_requisicao("encurtar", endereco_cliente)

        if not validar_url_original(url):
            return self._resposta(
                status="erro",
                mensagem="URL inválida. Use uma URL HTTP ou HTTPS completa.",
            )

        url = url.strip()

        try:
            codigo_existente = self.repositorio.buscar_por_url(url)
            if codigo_existente:
                return self._resposta(
                    status="existente",
                    url_original=url,
                    url_encurtada=f"{PREFIXO_URL}{codigo_existente}",
                )

            while True:
                codigo = gerar_codigo_aleatorio()
                if self.repositorio.inserir(url, codigo):
                    return self._resposta(
                        status="sucesso",
                        url_original=url,
                        url_encurtada=f"{PREFIXO_URL}{codigo}",
                    )

                codigo_existente = self.repositorio.buscar_por_url(url)
                if codigo_existente:
                    return self._resposta(
                        status="existente",
                        url_original=url,
                        url_encurtada=f"{PREFIXO_URL}{codigo_existente}",
                    )
        except sqlite3.DatabaseError as erro:
            print(
                f"[SERVIDOR {self.servidor_id}] Erro no banco: {erro}", flush=True
            )
            return self._resposta(
                status="erro", mensagem="Não foi possível acessar a base de dados."
            )

    def resolver(self, url_encurtada, endereco_cliente=None):
        self._registrar_requisicao("resolver", endereco_cliente)

        codigo = extrair_codigo(url_encurtada)
        if codigo is None:
            return self._resposta(
                status="erro",
                mensagem=f"URL encurtada inválida. Use {PREFIXO_URL}[8 caracteres].",
            )

        try:
            url_original = self.repositorio.buscar_por_codigo(codigo)
        except sqlite3.DatabaseError as erro:
            print(
                f"[SERVIDOR {self.servidor_id}] Erro no banco: {erro}", flush=True
            )
            return self._resposta(
                status="erro", mensagem="Não foi possível acessar a base de dados."
            )

        if url_original:
            return self._resposta(
                status="sucesso", codigo=codigo, url_original=url_original
            )

        return self._resposta(
            status="erro",
            mensagem=f"URL encurtada '{url_encurtada}' não encontrada na base de dados.",
        )


def validar_url_original(url):
    if not isinstance(url, str):
        return False
    url = url.strip()
    analisada = urlparse(url)
    return analisada.scheme in {"http", "https"} and bool(analisada.netloc)


def gerar_codigo_aleatorio():
    return "".join(secrets.choice(CARACTERES_CODIGO) for _ in range(8))


def extrair_codigo(url_encurtada):
    if not isinstance(url_encurtada, str):
        return None
    valor = url_encurtada.strip()
    codigo = valor[len(PREFIXO_URL) :] if valor.startswith(PREFIXO_URL) else valor
    if len(codigo) != 8 or not codigo.isalnum():
        return None
    return codigo


def criar_parser():
    parser = argparse.ArgumentParser(description="Servidor RPC do encurtador de URLs")
    parser.add_argument("servidor_id", type=int, choices=range(NUM_SERVIDORES))
    parser.add_argument("--host", default=ENDERECO_PADRAO)
    parser.add_argument("--porta-base", type=int, default=PORTA_BASE_PADRAO)
    parser.add_argument("--banco", type=Path, default=BANCO_PADRAO)
    return parser


def main():
    argumentos = criar_parser().parse_args()
    porta = argumentos.porta_base + argumentos.servidor_id
    repositorio = RepositorioURLs(argumentos.banco)
    servico = ServicoEncurtador(argumentos.servidor_id, repositorio)

    with ServidorXMLRPCConcorrente(
        (argumentos.host, porta),
        requestHandler=ManipuladorRPC,
        allow_none=True,
        logRequests=False,
    ) as servidor:
        servidor.register_function(servico.ping, "ping")
        servidor.register_function(servico.encurtar, "encurtar")
        servidor.register_function(servico.resolver, "resolver")

        print(
            f"[SERVIDOR {argumentos.servidor_id}] RPC iniciado em "
            f"{argumentos.host}:{porta}",
            flush=True,
        )
        print(
            f"[SERVIDOR {argumentos.servidor_id}] Banco: {repositorio.caminho_banco}",
            flush=True,
        )
        print(
            f"[SERVIDOR {argumentos.servidor_id}] Aguardando requisições...",
            flush=True,
        )
        servidor.serve_forever()


if __name__ == "__main__":
    main()
