from xmlrpc.server import SimpleXMLRPCServer

ENDERECO = "127.0.0.1"
PORTA= 8000

def somar(a, b):
    return a + b


def multiplicar(a, b):
    return a * b


servidor = SimpleXMLRPCServer( (ENDERECO, PORTA) )

servidor.register_function(somar, "somar")
servidor.register_function(multiplicar, "multiplicar")

print("Servidor RPC iniciado.")
print("Aguardando requisições...")

servidor.serve_forever()