#lang racket
(require examples)

(examples
 (check-equal? (quicksort (list 6 5 9 3 1 4 7 8 10 2)) (list 1 2 3 4 5 6 7 8 9 10))
 (check-equal? (quicksort empty) empty)
 (check-equal? (quicksort (list 1 2 3 4)) (list 1 2 3 4))
 (check-equal? (quicksort (list 1)) (list 1)))

(define (quicksort lst)
  (cond
    [(empty? lst)
     empty]
    [else
     (define pivo (first lst))
     (define resto-lst (rest lst))
     (define lst-menores (filter (lambda (x) (< x pivo)) resto-lst))
     (define lst-maiores (filter (lambda (x) (>= x pivo)) resto-lst))
     (append (quicksort lst-menores) (list pivo) (quicksort lst-maiores))]))