#lang racket
(require examples)
;; Função scan que aplica uma função binária f, com um valor inicial e uma lista de valores
;; e retorna uma lista onde cada elemento é o resultado parcial acumulado até aquele ponto.
;; (f valor-inicial lista -> lista acumulada)

(examples
 (check-equal? (scan + 0 (list 3 10 5)) (list 3 13 18))
 (check-equal? (scan * 1 (list 4 2 8 3)) (list 4 8 64 192))
 (check-equal? (scan - 200 (list 3 6 15 48)) (list 197 191 176 128))
 (check-equal? (scan append empty (list (list 1) (list 2) (list 3))) (list (list 1) (list 1 2) (list 1 2 3))))

(define (scan f valor-inicial lista)
  (define (aux-scan auxlista acumulado resultado)
    (cond
      [(empty? auxlista) (reverse resultado)]         
      [else 
       (let ([novo-acumulado (f acumulado (first auxlista))])
         (aux-scan (rest auxlista) novo-acumulado (cons novo-acumulado resultado)))])) 
  (aux-scan lista valor-inicial (list )))  



