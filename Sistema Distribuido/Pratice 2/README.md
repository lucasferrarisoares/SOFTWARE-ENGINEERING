# Load balancing graph analysis

Install the plotting dependency:

```powershell
python -m pip install matplotlib
```

Start each server in a separate terminal from this directory:

```powershell
python servidor.py 8001 A
python servidor.py 8002 B
python servidor.py 8003 C
```

In a fourth terminal, run each algorithm sequentially with the **same input**.
Wait for each run to finish before starting the next one:

```powershell
python balanceador.py rand entrada01.txt
python balanceador.py rr entrada01.txt
python balanceador.py lc entrada01.txt
python analise_grafica.py --title "Balanceamento de carga - entrada01.txt"
```

The analysis reads `log_rand.txt`, `log_rr.txt` and `log_lc.txt` and saves
`comparacao_algoritmos.png`. No graphical desktop is required. Stop the three
servers with Ctrl+C after the experiments.

Custom log paths and output names are also supported:

```powershell
python analise_grafica.py --rand resultados/entrada01/log_rand.txt --rr resultados/entrada01/log_rr.txt --lc resultados/entrada01/log_lc.txt --output resultados/entrada01/comparacao.png --title "Balanceamento de carga - entrada01.txt"
```

The figure shows the pending requests for servers A, B and C in each algorithm,
with identical axis scales, and compares each server's maximum observed count.
The current server processes requests sequentially, so pending counts include
queued requests as well as the one being processed.

Each log row is an event: either a dispatch or a completion. The horizontal axis
is therefore **event order, not milliseconds**; these logs cannot measure elapsed
time or average response time. Matching event numbers across algorithms do not
necessarily represent the same instant or request. Logs contain no input identity,
so the caller must ensure that all three runs use the same input.

Repeating an algorithm overwrites its log. Save each input's three logs in a
separate directory before running another experiment. Random choices can produce
different results between runs; a single graph is a comparison of those runs,
not a guarantee that one algorithm is always better.

---

# Análise gráfica do balanceamento de carga

Instale a dependência para gerar os gráficos:

```powershell
python -m pip install matplotlib
```

Na pasta desta atividade, inicie cada servidor em um terminal separado:

```powershell
python servidor.py 8001 A
python servidor.py 8002 B
python servidor.py 8003 C
```

Em um quarto terminal, execute os algoritmos em sequência usando o **mesmo arquivo de entrada**.
Aguarde cada execução terminar antes de iniciar a próxima:

```powershell
python balanceador.py rand entrada01.txt
python balanceador.py rr entrada01.txt
python balanceador.py lc entrada01.txt
python analise_grafica.py --title "Balanceamento de carga - entrada01.txt"
```

O script de análise lê `log_rand.txt`, `log_rr.txt` e `log_lc.txt` e salva o gráfico
em `comparacao_algoritmos.png`. A geração não exige uma interface gráfica.
Após os experimentos, encerre os três servidores com Ctrl+C em seus respectivos terminais.

Também é possível indicar os caminhos dos logs e o nome do arquivo de saída:

```powershell
python analise_grafica.py --rand resultados/entrada01/log_rand.txt --rr resultados/entrada01/log_rr.txt --lc resultados/entrada01/log_lc.txt --output resultados/entrada01/comparacao.png --title "Balanceamento de carga - entrada01.txt"
```

A figura mostra as requisições pendentes nos servidores A, B e C para cada algoritmo,
usando as mesmas escalas nos eixos, e compara o maior número de requisições pendentes
observado em cada servidor. Na implementação atual, cada servidor processa uma
requisição por vez; por isso, a contagem inclui tanto as requisições na fila quanto
a que está sendo processada.

Cada linha do log representa um evento: o envio ou a conclusão de uma requisição.
O eixo horizontal indica a **ordem dos eventos**, sem representar milissegundos.
Esses logs não permitem medir o tempo decorrido nem o tempo médio de resposta.
Eventos com o mesmo número em algoritmos diferentes não representam necessariamente
o mesmo instante ou a mesma requisição. Como os logs não identificam o arquivo de
entrada utilizado, quem executa os experimentos deve garantir que as três execuções
usem a mesma entrada.

Executar um algoritmo novamente sobrescreve seu log. Antes de iniciar outro
experimento, salve os três logs de cada entrada em uma pasta separada.
As escolhas aleatórias podem produzir resultados diferentes entre execuções.
Um gráfico compara as execuções realizadas, sem garantir que um algoritmo seja
sempre melhor que os demais.
