from xmlrpc.server import SimpleXMLRPCServer

ENDERECO = "127.0.0.1"
PORTA= 8000

def somar(a, b):
    return a + b

def multiplicar(a, b):
    return a * b

def subtrair(a, b):
    return a - b


def dividir(a, b):
    if b == 0:
        raise ValueError("Nao e possivel dividir por zero.")
    return a / b

servidor = SimpleXMLRPCServer( (ENDERECO, PORTA) )

servidor.register_function(somar, "somar")
servidor.register_function(multiplicar, "multiplicar")
servidor.register_function(subtrair, "subtrair")
servidor.register_function(dividir, "dividir")

print("Servidor RPC iniciado.")
print("Aguardando requisições...")

servidor.serve_forever()