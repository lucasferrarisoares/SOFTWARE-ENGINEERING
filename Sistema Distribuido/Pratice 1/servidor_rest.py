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

        try:
            a = float(params["a"][0])
            b = float(params["b"][0])

            if url.path == "/sum":
                resultado = a + b

            if url.path == "/mult":
                resultado = a * b

            if url.path == "/sub":
                resultado = a - b

            if url.path == "/div":
                if b == 0:
                    self.enviar_resposta(
                        400, {"erro": "Não é possível dividir por zero"}
                    )
                    return

                resultado = a / b

            self.enviar_resposta(200, {"resultado": resultado})


        except Exception as e:
            self.enviar_resposta(400, {"erro": "Erro na operação"})

    def enviar_resposta(self, code, response):

        msg = json.dumps(response).encode("utf-8")
        self.send_response(code)

        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg)

#codigo principal
servidor = HTTPServer((ENDERECO, PORTA), ServidorREST)

print("Servidor REST iniciado, aguardando requisições...")

servidor.serve_forever()
