#lang racket
(require examples)

(examples
 (check-equal? (lista-quadrada (list )) empty)
 (check-equal? (lista-quadrada (list 1)) (list 1))
 (check-equal? (lista-quadrada (list 1 2)) (list 1 4))
 (check-equal? (lista-quadrada (list 1 2 3)) (list 1 4 9))
 (check-equal? (lista-quadrada (list 2 5 3)) (list 4 25 9)))



(define (lista-quadrada lst)
  (cond
    [(empty? lst)
     empty]
    [else
     (cons (sqr (first lst)) (lista-quadrada (rest lst)))]))
 
 