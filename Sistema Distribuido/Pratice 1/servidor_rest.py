from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

ENDERECO = "127.0.0.1"
PORTA= 8000


class ServidorREST(BaseHTTPRequestHandler):

    def do_GET(self):
        
        url = urlparse(self.path)
        print(f"Requisição recebida: {url}")

        params = parse_qs(url.query)    

        return None


    def enviar_resposta(self, codigo, resposta):

        #implementar na aula
        return None


#codigo principal
servidor = HTTPServer((ENDERECO, PORTA), ServidorREST)

print("Servidor REST iniciado, aguardando requisições...")

servidor.serve_forever()
