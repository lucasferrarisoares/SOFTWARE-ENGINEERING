import sys
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class ServidorLocal:
    def __init__(self, linhaArqEntrada):
        partes = linhaArqEntrada.split()
        self.id = partes[0]
        self.rtt_prim_min = float(partes[1])
        self.rtt_prim_max = float(partes[2])
        self.max_usuario = int(partes[3])
        self.rtt_user_min = float(partes[4])
        self.rtt_user_max = float(partes[5])
        self.limiar_percentual = float(partes[6])

        self.limiar_absoluto = self.max_usuario * self.limiar_percentual / 100
        self.is_replica_ativa = False # Contra se a replica está ativa ou não no servidor

    def verificaReplicaDinamica(self, usuariosAtivos):
        if usuariosAtivos >= self.limiar_absoluto:
            self.is_replica_ativa = True
        else:
            self.is_replica_ativa = False

    def simulaRTT(self):
        rtt_usuario_servidor = random.uniform(self.rtt_user_min, self.rtt_user_max)

        if self.is_replica_ativa:
            return rtt_usuario_servidor
        else:
            rtt_servidor_primario = random.uniform(self.rtt_prim_min, self.rtt_prim_max)
            return rtt_usuario_servidor + rtt_servidor_primario

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

    resultados_media_rtt = {}
    for s in servidores:
        resultados_media_rtt[s.id] = []

    for unidade_tempo in range(t):
        for i_servidor, servidor in enumerate(servidores):
            usuarios_solic_req = cargasTrabalho[i_servidor] [unidade_tempo]
            servidor.verificaReplicaDinamica(usuarios_solic_req)

            rtts_iteracao = []
            for i in range(usuarios_solic_req):
                rtt = servidor.simulaRTT()
                rtts_iteracao.append(rtt)


            media_rtt = 0
            if usuarios_solic_req > 0:
                media_rtt = sum(rtts_iteracao) / usuarios_solic_req

            resultados_media_rtt[servidor.id].append(media_rtt)

    return resultados_media_rtt



def plotar_grafico(resultados, t):
    figure, axis = plt.subplots(figsize=(10, 6), layout="constrained")
    tempos = range(1, t + 1)

    for servidor_id, serie in resultados.items():
        axis.plot(tempos, serie, marker="o", label=f"Servidor {servidor_id}")

    axis.set_title("Média de RTT por servidor ao longo do tempo")
    axis.set_xlabel("Unidade de tempo")
    axis.set_ylabel("RTT médio (ms)")
    axis.grid(alpha=0.2)
    if resultados:
        axis.legend()

    try:
        figure.savefig("series_rtt.png", dpi=160)
    finally:
        plt.close(figure)

    return None


if __name__ == "__main__":
    
    arqEntrada = sys.argv[1]
    servidores, t, cargasTrabalho = carregarComponentes(arqEntrada)
    logs = simular(servidores, t, cargasTrabalho)
    plotar_grafico(logs, t)
