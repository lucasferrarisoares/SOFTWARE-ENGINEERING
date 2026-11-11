"""Visitador da AST, seguindo a organização da Prática 4 (RoboDIN)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import nos_ast as ast


class Visitador:
    def visita(self, no: ast.No):
        if no is None:
            return
        nome_metodo = f"visita_{type(no).__name__}"
        visitador = getattr(self, nome_metodo, self.visita_padrao)
        return visitador(no)

    def visita_padrao(self, no: ast.No):
        raise NotImplementedError(f"visita_{type(no).__name__} não foi implementada.")
