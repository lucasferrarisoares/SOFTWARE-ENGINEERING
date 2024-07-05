#lang racket
(require examples)

;;Função que retorna a soma de todos o números naturais entre 0 e n
;;
;; NumeroNatural --> NumeroNatural

(examples
 (check-equal? (soma-ate 4) 10)
 (check-equal? (soma-ate 10) 55)
 (check-equal? (soma-ate 3) 6)
 (check-equal? (soma-ate 0) 0))

(define (soma-ate n)
  (cond
    [(zero? n)
    0]
    [(+ n (soma-ate (sub1 n)))]))