import sys
import random

class ServidorLocal:
    def __init__(self, linhaArqEntrada):
        #TODO
        return None

    def verificaReplicaDinamica(self, usuariosAtivos):
        #TODO
        return None

    def simulaRTT(self):
        #TODO
        return None

def carregarComponentes(caminhoArq):
    with open(caminhoArq, 'r') as f:
        linhas = f.readlines()
        n = int(linhas.pop(0).strip())
        servidores = []

        for i in range(n):
            linhaArqEntrada = linhas.pop(0).strip()
            servidores.append(ServidorLocal(linhaArqEntrada))
        
        t = int(linhas.pop(0).strip())
        
        cargasTrabalho = []
        for i in range(n):
            cargaLinha = linhas.pop(0).strip().split()
            cargasTrabalho.append([int(val) for val in cargaLinha])
            
        return servidores, t, cargasTrabalho


def simular(servidores, t, cargasTrabalho):
    #TODO
    return None

def plotar_grafico(resultados, t):
   #TODO
    return None


if __name__ == "__main__":
    
    arqEntrada = sys.argv[1]
    servidores, t, cargasTrabalho = carregarComponentes(arqEntrada)
    logs = simular(servidores, t, cargasTrabalho)
    plotar_grafico(logs, t)