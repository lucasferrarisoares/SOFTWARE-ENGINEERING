#lang racket
(require examples)
;; Salário é um numerico
;; Salario -> Salario

;; Calcula o novo salario com base no salario atual
;; Se for <= 1200.00 o novo salario recebara aumento de 10%
;; Se for > 1200.00 e < 3000.00 recebera aumento de 7%
;; Se for > 3000.00 e <= 8000.00 recebra aumento de 3%
;; Caso seja > 8000.00 nao recebera aumento.

(examples)
 

(define (novo-salario salario-atual)
 (cond
   [(<=  salario-atual 1200.00) (* salario-atual 1.10)]
   [(<= salario-atual 3000.00) (* salario-atual 1.07)]
   [(<= salario-atual 8000.00) (* salario-atual 1.03)]
   [else salario-atual]))