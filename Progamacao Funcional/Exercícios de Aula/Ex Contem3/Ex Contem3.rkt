#lang racket
(require examples)


(examples
 (check-equal? (contem-3 (list )) #f)
 (check-equal? (contem-3 (list 1 2 4)) #f)
 (check-equal? (contem-3 (list 1 2 3 4)) #t)
 (check-equal? (contem-3 (list 1 2 3)) #t))


 (define (contem-3 lst)
   (cond
     [(empty? lst)
      #f]
     [(equal? (first lst) 3)
      #t]
     [else
      (contem-3 (rest lst))]))