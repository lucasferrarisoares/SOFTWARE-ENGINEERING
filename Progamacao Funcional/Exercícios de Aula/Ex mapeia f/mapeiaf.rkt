#lang racket
(require examples)

;; Funçao de alta ordem que receba uma lista lst e uma outra funcao f(x) e aplica
;; f(x) em cada elemento da lista lst

(examples
 (check-equal? (mapeia add1 empty) empty)
 (check-equal? (mapeia add1 (list 4)) (list 5))
 (check-equal? (mapeia add1 (list 4 7)) (list 5 8))
 (check-equal? (mapeia sqr (list 3 7)) (list 9 49))
 (check-equal? (mapeia string-length (list "ola" "mundo" "com" "funcao" "de" "alta" "ordem")) (list 3 5 3 6 2 4 5)))
 


(define (mapeia f lst)
  (cond
    [(empty? lst)
     empty]
    [else
     (cons (f (first lst)) (mapeia f (rest lst)))]))