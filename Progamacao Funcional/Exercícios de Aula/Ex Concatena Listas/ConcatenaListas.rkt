#lang racket
(require examples)

;; Funcao que receb duas listas de numeros e faz a
;; concatenacao entre ambas

;; list list -> list

(examples
 (check-equal? (concatena (list 1 2) empty) (list 1 2))
 (check-equal? (concatena empty (list 3 4)) (list 3 4))
 (check-equal? (concatena empty empty) empty)
 (check-equal? (concatena (list 1 2 3) (list 4 5 6)) (list 1 2 3 4 5 6))
 (check-equal? (concatena (list 1 2) (list 3 4)) (list 1 2 3 4))
 (check-equal? (concatena (list 7 8) (list 5 6)) (list 7 8 5 6))
 (check-equal? (concatena (list 1) (list 4 5)) (list 1 4 5)))
 

(define (concatena lst-a lst-b)
  (cond
    [(empty? lst-a)
     lst-b]
    [else
     (cons (first lst-a) (concatena (rest lst-a) lst-b))]))