from urllib.parse import urlparse
from xmlrpc.client import SafeTransport, ServerProxy, Transport


class TransporteComTimeout(Transport):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def make_connection(self, host):
        conexao = super().make_connection(host)
        conexao.timeout = self.timeout
        return conexao


class TransporteSeguroComTimeout(SafeTransport):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def make_connection(self, host):
        conexao = super().make_connection(host)
        conexao.timeout = self.timeout
        return conexao


class ProxyRPC:
    def __init__(self, url, transporte):
        self._proxy = ServerProxy(url, transport=transporte, allow_none=True)
        self._fechado = False

    def __getattr__(self, nome):
        return getattr(self._proxy, nome)

    def close(self):
        if not self._fechado:
            self._proxy.__exit__(None, None, None)
            self._fechado = True

    def __enter__(self):
        return self

    def __exit__(self, tipo, valor, traceback):
        self.close()


def criar_proxy(url, timeout=10.0):
    esquema = urlparse(url).scheme.lower()
    if esquema == "https":
        transporte = TransporteSeguroComTimeout(timeout)
    elif esquema == "http":
        transporte = TransporteComTimeout(timeout)
    else:
        raise ValueError("A URL RPC deve começar com http:// ou https://")

    return ProxyRPC(url, transporte)
