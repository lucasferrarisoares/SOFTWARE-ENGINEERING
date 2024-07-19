#lang racket
(require examples)

;; Função que recebe um valor natural e retorna o fatiral deste valor
;; Natural -> Natural

(examples
 (check-equal? (fatorial 6) 720)
 (check-equal? (fatorial 3) 6)
 (check-equal? (fatorial 0) 1)
 (check-equal? (fatorial 1) 1))

(define (fatorial n)
  (cond
    [(<= n 0)
     1]
    [else
     (* (fatorial (sub1 n)) n)]))



;;Função que recebe uma lista de naturais lst e retorna uma lista ret onde o i-ésimo
;;elemento de ret é dado pelo fatorial do i-ésimo elemento de lst

(examples
 (check-equal? (fatoriaislist (list 1 2 3 4)) (list 1 2 6 24))
 (check-equal? (fatoriaislist (list 3 1)) (list 6 1))
 (check-equal? (fatoriaislist (list )) (list ))
 (check-equal? (fatoriaislist (list 5)) (list 120)))

;; list -> list

(define (fatoriaislist lst)
  (cond
    [(empty? lst)
     empty]
    [else
     (cons (fatorial (first lst)) (fatoriaislist (rest lst)))]))