#lang racket
(require examples)

;;Função que recebe uma lista de números e um número x, e soma x
;; em todos os elemtnso da lista

(examples
 (check-equal? (soma-x (list ) 5) (list ))
 (check-equal? (soma-x (list 7) 2) (list 9))
 (check-equal? (soma-x (list 10 15 20 25) 5) (list 15 20 25 30))
 (check-equal? (soma-x (list 1 2 3 4) -2) (list -1 0 1 2))
 (check-equal? (soma-x (list 9 0 3 1) 10) (list 19 10 13 11)))



(define (soma-x ldn x)
  ;;verificamos se a lista está vazia
  ;;caso base
  (cond
    [(empty? ldn) empty]
    [else
     ;;soma x ao elemento da lista e adiciona ele em uma nova lista.
     (cons (+ (first ldn) x)
          (soma-x (rest ldn) x))]))