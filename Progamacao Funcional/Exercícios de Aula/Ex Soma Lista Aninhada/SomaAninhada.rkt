#lang racket
(require examples)

;;Função que recebe uma ListaAninhada de numeros e soma todos os
;; elementos desta lista

(examples
 (check-equal? (soma-lst-aninhada (list 1 4 (list 5 empty (list 2) 9) 10)) 31)
 (check-equal? (soma-lst-aninhada (list (list 3 4) (list 5 6) (list 2 3))) 23)
 (check-equal? (soma-lst-aninhada (list 1 2 3 4)) 10)
 (check-equal? (soma-lst-aninhada (list )) 0)
 (check-equal? (soma-lst-aninhada (list (list ) (list ) (list ))) 0))

;;ListaAninhada -> Numero

(define (soma-lst-aninhada la)
 (cond
   [(empty? la)
    0]
   [(list? (first la))
    (+ (soma-lst-aninhada (first la))
       (soma-lst-aninhada (rest la)))]
   [else
    (+ (first la)
       (soma-lst-aninhada (rest la)))]))