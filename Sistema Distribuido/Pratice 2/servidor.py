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

    #exemplo de mensagem recebida: REQUEST;1;10
    
    #implementar o tratamento da mensagem

    print(f"[Servidor {rotulo}] finalizou {id_requisicao}")

sock.close()
