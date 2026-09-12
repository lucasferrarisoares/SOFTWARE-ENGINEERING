import random
import socket
import sys
import threading
import time

#inicializacao:
# python balanceador.py [estrategia de balanceamento] [arq_entrada de entrada]
# estrategia de balanceamento pode ser: rand; rr ou lc

host = "127.0.0.1"
porta = 8000
intervalo_em_ms = 10
tam_buffer_udp = 1500

SERVIDORES = {
    "A": (host, 8001),
    "B": (host, 8002),
    "C": (host, 8003),
}


def aplicar_balanceamento():
    global indice_rr

    with lock:
        #implementar na aula
        return None


def receber_finalizacoes():
    while True:
        dados, _ = sock.recvfrom(tam_buffer_udp)
        mensagem = dados.decode().strip()

        partes = mensagem.split(";")
        if len(partes) != 3 or partes[0] != "DONE":
            continue

        _, id_requisicao, servidor = partes

        with lock:
            if ativos[servidor] > 0:
                ativos[servidor] -= 1

            print(f"[Balanceador] {id_requisicao} terminou no servidor {servidor}")
            registrar_log()


def carregar_requisicoes():
    requisicoes = []

    with open(arq_entrada, "r", encoding="utf-8") as arq:
        for numero, linha in enumerate(arq, 1):
            linha = linha.strip()

            if not linha:
                continue

            partes = linha.split(";")
            if len(partes) != 2:
                raise ValueError(f"Linha {numero} inválida: {linha}")

            id_requisicao = partes[0]
            tempo = int(partes[1])

            requisicoes.append((id_requisicao, tempo))

    return requisicoes


def registrar_log():
    linha = f"{ativos['A']};{ativos['B']};{ativos['C']}"
    log.write(linha + "\n")
    log.flush()


if __name__ == '__main__':

    estrat_balanceamento = sys.argv[1].lower()
    arq_entrada = sys.argv[2]

    #inicialização do socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, porta))


    #inicializacoes de estruturas auxiliares de cada estrategia
    ativos = {"A": 0, "B": 0, "C": 0}
    indice_rr = 0
    lock = threading.Lock()

    log = open(f"log_{estrat_balanceamento}.txt", "w", encoding="utf-8")

    requisicoes = carregar_requisicoes()

    threading.Thread(target=receber_finalizacoes, daemon=True).start()

    for id_requisicao, tempo in requisicoes:

        #implementar a lógica de balanceamento e envio para o servidor
        

    #aguardando a finalização de todas as tarefas por parte dos servidores
    while True:
        with lock:
            total = sum(ativos.values())

        if total == 0:
            break

        time.sleep(0.01)

    print("Todas as requisições foram concluídas.")

    log.close()
    sock.close()
