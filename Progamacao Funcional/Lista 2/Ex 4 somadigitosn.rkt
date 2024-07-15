#lang racket
(require examples)

;; Receber um valor natural, e somar todos os seus algoritimos.
;; int -> int;

(examples
 (check-equal? (soma-digitos 1234) 10)
 (check-equal? (soma-digitos  27) 9)
 (check-equal? (soma-digitos  6) 6)
 (check-equal? (soma-digitos  0) 0)
 (check-equal? (soma-digitos  7869) 30))

(define (soma-digitos n)
  (cond
    [( <= n 9) n]
    [else
     (+ (remainder n 10) (soma-digitos (quotient n 10)))]))