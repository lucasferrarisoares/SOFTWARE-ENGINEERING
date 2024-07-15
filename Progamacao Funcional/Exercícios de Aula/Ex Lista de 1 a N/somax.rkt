#lang racket
(require examples)

;; função que recebe um valor x e uma lista lst, e coloque x na ultima posição de lst
;; numero lista -> lista

(examples
 (check-equal? (adiciona-fim 4 (list 1 2)) (list 1 2 4))
 (check-equal? (adiciona-fim 2 (list 1)) (list 1 2))
 (check-equal? (adiciona-fim  1 (list )) (list 1)))
 

(define (adiciona-fim x lst)
  (cond
  [(empty? lst) (cons x empty)]
  [else
   (cons (first lst) (adiciona-fim x (rest lst)))]))



;; Função que reccebe um valor natural n, e gera uma lista
;; com todos os elemntos naturais entre 1 e n

;; Natural -> lista

(examples
 (check-equal? (lista-natural 3) (list 1 2 3))
 (check-equal? (lista-natural 2) (list 1 2))
 (check-equal? (lista-natural 1) (list 1))
 (check-equal? (lista-natural 0) (list )))

(define (lista-natural n)
  (cond
    [(zero? n) empty]
    [else
     (adiciona-fim n (lista-natural (sub1 n)))]))