from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Pessoa:
    Nome: str
    Idade: int
    Sexo: str
    Peso: float

@dataclass
class No:
    elemento: Pessoa
    altura: int = 0
    filhoEsq: No | None = None
    filhoDir: No | None = None

class AVL:
    " Representa uma árvore AVL"
    def __init__(self):
        self.raiz: No | None = None

    def vazia(self):
        return self.raiz == None
    
    # calcula o FB do nó
    def _fb(self, no: No) -> int:
        if no == None:
            return 0
        altSAE = -1
        altSAD = -1
        if no.filhoEsq != None:
            altSAE = no.filhoEsq.altura
        if no.filhoDir != None:
            altSAD = no.filhoDir.altura
        return altSAD - altSAE

    # atualiza a altura do nó
    def _atualizaAltura(self, no: No) -> None:
        if no != None:
            altSAE = -1
            altSAD = -1
            if no.filhoEsq != None:
                altSAE = no.filhoEsq.altura
            if no.filhoDir != None:
                altSAD = no.filhoDir.altura
            no.altura = max(altSAE, altSAD) + 1

    # faz rotação simples para a esquerda
    def _rotacionaEsq(self, pai: No) -> No:
        if pai == None:
            raise ValueError('Referência inválida')
        filho = pai.filhoDir
        pai.filhoDir = filho.filhoEsq
        filho.filhoEsq = pai
        self._atualizaAltura(pai)
        self._atualizaAltura(filho)
        return filho
    
    # faz rotação simples para a direita
    def _rotacionaDir(self, pai: No) -> No:
        if pai == None:
            raise ValueError('Referência inválida')
        filho = pai.filhoEsq
        pai.filhoEsq = filho.filhoDir
        filho.filhoDir = pai
        self._atualizaAltura(pai)
        self._atualizaAltura(filho)
        return filho
    
    # faz o balanceamento do nó
    def _balanceia(self, no: No) -> No | None:
        if no != None:
            # desbalanceado para a direita
            if self._fb(no) == 2:
                if self._fb(no.filhoDir) == -1:
                    no.filhoDir = self._rotacionaDir(no.filhoDir) 
                # rotaciona para a esquerda
                no = self._rotacionaEsq(no)
            # desbalanceado para a esquerda
            elif self._fb(no) == -2:
                if self._fb(no.filhoEsq) == 1:
                    no.filhoEsq = self._rotacionaEsq(no.filhoEsq)
                # rotaciona para a direita
                no = self._rotacionaDir(no)
        return no

    def insere(self, elem: Pessoa) -> None:
        self.raiz = self._insereNo(elem, self.raiz)

    def _insereNo(self, elem: Pessoa, raiz: No) -> No:
        if raiz == None:
            raiz = No(elem)
        else:
            if elem.Nome < raiz.elemento.Nome:
                raiz.filhoEsq = self._insereNo(elem, raiz.filhoEsq)            
            elif elem.Nome > raiz.elemento.Nome:
                raiz.filhoDir = self._insereNo(elem, raiz.filhoDir)
            # rebalanceando
            self._atualizaAltura(raiz)
            raiz = self._balanceia(raiz)
        return raiz
    
    def remove(self, elem: Pessoa) -> None:
          self.raiz = self._removeNo(elem, self.raiz)
     
    def _removeNo(self, elem: Pessoa, raiz: No) -> No | None:
        if raiz != None:
            if elem.Nome < raiz.elemento.Nome:
                raiz.filhoEsq = self._removeNo(elem, raiz.filhoEsq)


    def exibe(self) -> None:
        self._exibeNo(self.raiz)
        print()
    
    def _exibeNo(self, raiz: No) -> None:
        if raiz != None:
            print('(', end='')
            self._exibeNo(raiz.filhoEsq)
            print(' ', raiz.elemento.Nome, ' ', end='')
            self._exibeNo(raiz.filhoDir)
            print(')', end='')

    def busca(self, elem: Pessoa) -> No | None:
        return self._buscaNo(elem, self.raiz)
    
    def _buscaNo(self, elem: Pessoa, raiz: No) -> No | None:
        if raiz != None:
            if elem.Nome == raiz.elemento.Nome:
                return raiz
            elif elem.Nome < raiz.elemento.Nome:
                return self._buscaNo(elem, raiz.filhoEsq)
            else:
                return self._buscaNo(elem, raiz.filhoDir)
        else:
            return None

def cadastrarsimples():
    nome = (str(input('\nInsira aqui, a pessoa que deve ser cadastrada no sistema: ')))
    idade = (int(input('\nQual a idade da pessoa: ')))
    sexo = (str(input('\nQual sexo da pessoa(F/M): ')))
    peso = (float(input('\nQual peso da pessoa: ')))

    Pessoa1 = Pessoa(nome.upper(), idade, sexo.upper(), peso)
    
    BancoCadastro.insere(Pessoa1)   
    return  

def cadastrolote():
    pessoas = input('\nInsira aqui, as pessoas que devem ser cadastradas no sistema, seprando as pessoas por ;\n ')
    listaPessoas = pessoas.split(sep=';')
    for p in listaPessoas:
        (nome, idade, sexo, peso) = p.split(sep=',')
        pessoa = Pessoa(nome.upper(), int(idade), sexo.upper(), float(peso))
        BancoCadastro.insere(pessoa)
    return 

def buscanome():
    nomeprocura = (str(input('\nPor qual pessoa você está procurando(Digite apenas o nome): ')))
    Pessoabusca = Pessoa(nomeprocura.upper(), 0, 'M', 0)
    pessoa_encontrada = BancoCadastro.busca(Pessoa(nomeprocura.upper(), 0, 'M', 0))
    if pessoa_encontrada:
        print("Pessoa encontrada:")
        print(pessoa_encontrada.elemento)
    else:
        print("Pessoa não encontrada.")
    return

def relatorio():
    print("\nRelatório:")
    if BancoCadastro.vazia():
        print("Não há pessoas cadastradas.")
    else:
        print("Nomes cadastrados em ordem alfabética:")
        BancoCadastro.exibe()
        total_pessoas = _contar_pessoas(BancoCadastro.raiz)
        print(f"Total de pessoas cadastradas: {total_pessoas}")
        homens, mulheres = _contar_sexos(BancoCadastro.raiz)
        print(f"Quantidade de homens: {homens}")
        print(f"Quantidade de mulheres: {mulheres}")
        peso_medio = _calcular_peso_medio(BancoCadastro.raiz)
        print(f"Peso médio das pessoas cadastradas: {peso_medio:.2f}")
        maiores_18 = _contar_maiores_dezoito(BancoCadastro.raiz)
        print(f"Número de pessoas maiores de 18 anos: {maiores_18}")

def _contar_pessoas(raiz: No) -> int:
    if raiz is None:
        return 0
    return 1 + _contar_pessoas(raiz.filhoEsq) + _contar_pessoas(raiz.filhoDir)

def _contar_sexos(raiz: No) -> tuple[int, int]:
    if raiz is None:
        return 0, 0
    homens_esq, mulheres_esq = _contar_sexos(raiz.filhoEsq)
    homens_dir, mulheres_dir = _contar_sexos(raiz.filhoDir)
    if raiz.elemento.Sexo == 'M':
        homens_esq += 1
    else:
        mulheres_esq += 1
    return homens_esq + homens_dir, mulheres_esq + mulheres_dir

def _calcular_pesototal(raiz: No) -> float:
    if raiz is None:
        return 0
    total_pesos = raiz.elemento.Peso
    total_pesos += _calcular_pesototal(raiz.filhoEsq)
    total_pesos += _calcular_pesototal(raiz.filhoDir)
    return total_pesos

def _calcular_peso_medio(raiz: No) -> float:
    PT = _calcular_pesototal(BancoCadastro.raiz)
    TP = _contar_pessoas(BancoCadastro.raiz)
    return PT / TP


def _contar_maiores_dezoito(raiz: No) -> int:
    if raiz is None:
        return 0
    maiores_esq = _contar_maiores_dezoito(raiz.filhoEsq)
    maiores_dir = _contar_maiores_dezoito(raiz.filhoDir)
    idade = raiz.elemento.Idade
    return (idade > 18) + maiores_esq + maiores_dir

BancoCadastro = AVL()

def main():
    print()
    
    while True:
        print()
        print('\nMenu:')
        print('A. Cadastro;')
        print('B. Busca;')
        print('C. Relatório;')
        print('D; Sair.')

        opcao = input('Olá, seja bem-vindo, qual opção deseja selecionar? ')

        if opcao.upper() == 'A':
            tipocadastro = input('\nQual tipo de cadastro vamos realizar? (Simples/Lote): ')

            if tipocadastro.upper() == 'SIMPLES':
                print
                cadastrarsimples()
            elif tipocadastro.upper() == 'LOTE':
                print()
                cadastrolote()

        elif opcao.upper() == 'B':
            buscanome()
        elif opcao.upper() == 'C':     
            relatorio()
        elif opcao.upper() == 'D':
            print()
            print("Fechando o modo operação.")
            print()
            break
        else:
            print("Opção inválida. Tente novamente.")

main()