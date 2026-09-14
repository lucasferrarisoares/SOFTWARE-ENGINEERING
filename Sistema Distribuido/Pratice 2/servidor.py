import socket
import sys
import time

#inicializacao:
# python servidor.py [porta] [rotulo]
# Para ficar condizente com o balanceador, utilizar as combinações:
# 8001 A
# 8002 B
# 8003 C

host = "127.0.0.1"

porta = int(sys.argv[1])
rotulo = sys.argv[2]
tam_buffer_udp = 1500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, porta))

print(f"[Servidor {rotulo}] ouvindo em {host}:{porta}")

while True:
    dados, endereco = sock.recvfrom(tam_buffer_udp)
    mensagem = dados.decode().strip()

    partes = mensagem.split(";") 

    id_requisicao = partes[1]
    tempo = float(partes[2])

    print (f"Processando a requisicao {id_requisicao} por {tempo}")
    time.sleep(tempo / 1000)

    resposta = f"DONE;{id_requisicao};{rotulo}"
    sock.sendto(resposta.encode(), endereco)

    print(f"[Servidor {rotulo}] finalizou {id_requisicao}")

sock.close()
