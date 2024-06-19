#lang racket
(require examples)
(examples (check-equal? (combustivel 3 4) "Gasolina"))

(define (combustivel preco-alcool preco-gasolina)
  (if (>= (* preco-alcool 0.7) preco-gasolina)
          "Alcool"
          "Gasolina"))