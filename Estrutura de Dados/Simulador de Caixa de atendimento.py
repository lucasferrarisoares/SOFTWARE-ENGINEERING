class FilaAtendimento:
    def __init__(self):
        self.clientes_preferenciais = []
        self.clientes_comuns = []

    def adicionar_cliente(self, tipo_cliente, senha):
        if tipo_cliente == 'p':
            self.clientes_preferenciais.append(senha)
        elif tipo_cliente == 'c':
            self.clientes_comuns.append(senha)

    def chamar_proximo_cliente(self):
        if self.clientes_preferenciais:
            return self.clientes_preferenciais.pop(0), 'preferencial'
        elif self.clientes_comuns:
            return self.clientes_comuns.pop(0), 'comum'
        else:
            return None, None

    def consultar_clientes_em_espera(self):
        return {
            'preferencial': self.clientes_preferenciais,
            'comum': self.clientes_comuns
        }


class Caixa:
    def __init__(self, numero):
        self.numero = numero
        self.cliente_atendido = None

    def atender_cliente(self, cliente):
        self.cliente_atendido = cliente


def gerar_senha(tipo_cliente, fila):
    senha = len(fila.clientes_preferenciais) + len(fila.clientes_comuns) + 1
    fila.adicionar_cliente(tipo_cliente, senha)
    return senha


def chamar_cliente(caixas, fila):
    for caixa in caixas:
        senha, tipo_cliente = fila.chamar_proximo_cliente()
        if senha is not None:
            caixa.atender_cliente(senha)
            print(f'Caixa {caixa.numero} chamou o próximo cliente: {tipo_cliente} - Senha {senha}')
        else:
            print(f'Caixa {caixa.numero} está livre.')


def consultar_clientes_em_espera(fila):
    clientes_em_espera = fila.consultar_clientes_em_espera()
    print("Clientes preferenciais em espera:", clientes_em_espera['preferencial'])
    print("Clientes comuns em espera:", clientes_em_espera['comum'])


def consultar_estado_caixas(caixas):
    for caixa in caixas:
        if caixa.cliente_atendido is not None:
            print(f'Caixa {caixa.numero} está atendendo o cliente: Senha {caixa.cliente_atendido}')
        else:
            print(f'Caixa {caixa.numero} está livre.')


def main():
    print()
    num_caixas = int(input("Digite a quantidade de caixas:(Min:2 Max:20) \n"))
    fila_atendimento = FilaAtendimento()
    caixas = [Caixa(numero) for numero in range(1, num_caixas + 1)]

    if num_caixas < 2:
        raise ValueError('Número de caixas menor que o caixa mínimo, tente novamente com um número superior a 2.')
    elif num_caixas > 20:
        raise ValueError('Número de caixas superior ao de caixas máximos, tente novamente com um número inferior a 20.')

    while True:
        print()
        print("\nMenu:")
        print("A. Gerar senha")
        print("B. Chamar cliente")
        print("C. Consultar clientes em espera")
        print("D. Consultar estado dos caixas")
        print("E. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == 'A':
            print()
            tipo_cliente = input("Qual perfil você se enquadra (c/p): ")
            senha = gerar_senha(tipo_cliente, fila_atendimento)
            print()
            print(f'Senha gerada: {senha}')

        elif opcao == 'B':
            print()
            chamar_cliente(caixas, fila_atendimento)

        elif opcao == 'C':
            print()
            consultar_clientes_em_espera(fila_atendimento)

        elif opcao == 'D':
            print()
            consultar_estado_caixas(caixas)

        elif opcao == 'E':
            print()
            print("Saindo do simulador.")
            print()
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
