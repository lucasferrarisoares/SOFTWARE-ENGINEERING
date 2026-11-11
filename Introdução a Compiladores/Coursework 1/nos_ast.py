"""Nós da AST Coda; delimitadores e parênteses não geram nós."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# Classes base
@dataclass
class No:
    linha: int = field(kw_only=True)


@dataclass
class Comando(No):
    """Base dos comandos, sem comportamento de execução."""


@dataclass
class Expressao(No):
    """Base das expressões, ainda sem anotação de tipo semântico."""


# Programa e declarações
@dataclass
class Programa(No):
    nome: str
    globais: list[DeclaracaoVariavel]
    funcoes: list[Funcao]
    comandos: list[Comando]


@dataclass
class DeclaracaoVariavel(No):
    nome: str
    tipo: str


@dataclass
class Parametro(No):
    nome: str
    tipo: str


@dataclass
class Funcao(No):
    nome: str
    parametros: list[Parametro]
    tipo_retorno: str
    locais: list[DeclaracaoVariavel]
    comandos: list[Comando]


# Expressões
@dataclass
class Identificador(Expressao):
    nome: str


@dataclass
class Inteiro(Expressao):
    valor: int


@dataclass
class Booleano(Expressao):
    valor: bool


@dataclass
class OperacaoBinaria(Expressao):
    operador: Literal["+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!=", "&&", "||"]
    esquerdo: Expressao
    direito: Expressao


@dataclass
class OperacaoUnaria(Expressao):
    operador: Literal["-", "!"]
    operando: Expressao


@dataclass
class Chamada(Expressao):
    nome: str
    argumentos: list[Expressao]


# Comandos
@dataclass
class Atribuicao(Comando):
    destino: Identificador
    expressao: Expressao


@dataclass
class Condicional(Comando):
    condicao: Expressao
    entao: list[Comando]
    senao: list[Comando] | None


@dataclass
class Repeticao(Comando):
    condicao: Expressao
    comandos: list[Comando]


@dataclass
class Retorno(Comando):
    expressao: Expressao


@dataclass
class Leitura(Comando):
    identificadores: list[Identificador]


@dataclass
class Escrita(Comando):
    expressoes: list[Expressao]


@dataclass
class ChamadaComando(Comando):
    chamada: Chamada
