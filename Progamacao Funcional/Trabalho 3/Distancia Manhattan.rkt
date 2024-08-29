#lang racket
(require examples)


;;Calcula a distância euclidiana entre
;;dois pontos, p e q, ambos representados
;;como listas.
;;
;; List List -> Number
(define (distancia-manhattan p q)
 (cond
   [(or (empty? p) (empty? q))
    0]
 [else
  (+ (abs (- (first p) (first q)))
 (distancia-manhattan (rest p) (rest q)))]))

;; Recebe uma lista de numeros e devolve o menor numero
;; Lista(numeros) -> Numbero
(define (menor lst)
  (cond
    [(empty? lst) empty]
    [(empty? (rest lst)) (first lst)]
    [else (min (first lst) (menor (rest lst)))]))

;; Recebe uma lista de números e um número x, vai remover a primeira ocorrencia desse número x da lista
;; Numero Lista(números) -> Lista(números)
(define (remover x lst)
  (cond
    [(empty? lst) empty]
    [(equal? x (first lst)) (rest lst)]
    [else (cons (first lst) (remover x (rest lst)))]))

;; Função que recebe uma lista de números e devolve de forma ordenada
;; List -> List
(define (ordenar lst)
  (cond
    [(empty? lst) empty]
    [else
     (cons (menor lst) 
           (ordenar (remover (menor lst) lst)))]))

;; Função que retorna os k primeiros elementos de uma lista
;; List Number -> List
(define (k-primeiros lst k)
  (cond
    [(or (empty? lst) (<= k 0)) empty]  
    [else
     (cons (first lst)                  
           (k-primeiros (rest lst) (- k 1)))]))


;; Recebe uma lista de pontos e um ponto, e retorna qual a menor distância entre os ponto da lista e o ponto indicado
;; Lista(Pontos) ponto -> Menor Distância
;; list list -> int

(examples
  (check-equal? (distancias (list 3 4) (list (list 1 2) (list 3 4) (list 5 6)) 2 distancia-manhattan) (list 0 4))
  (check-equal? (distancias (list 3 2) (list (list 1 2) (list 3 4) (list 5 6)) 1 distancia-manhattan) (list 2))
  (check-equal? (distancias (list 25 25) (list (list 10 10) (list 20 20) (list 30 30)) 3 distancia-manhattan) (list 30 10 10)))

(define (distancias ponto lista-de-pontos k distancia-ponto)
  (define listdist (cond
    [(empty? lista-de-pontos)
     empty]
    [else
     (cons (distancia-ponto (first lista-de-pontos) ponto) (distancias ponto (rest lista-de-pontos) k distancia-ponto))]))
  (k-primeiros (ordenar listdist) k))  
  
  