#lang racket
(require examples)


;; Funçção que recebe duas listas de numeros, lst-valor e lst-peso,
;; para essa função, assume-se que lst-valor e lst-peso tem o mesmo tamanho


(examples
 (check-equal? (soma-ponderada empty empty) 0)
 (check-equal? (soma-ponderada (list 1 2 3) (list 1 2 3)) 14)
 (check-equal? (soma-ponderada (list 4 3 1) (list 2 4 5)) 25)
 (check-equal? (soma-ponderada (list 2) (list 0)) 0))

;; list list -> number;
 (define (soma-ponderada lst-valor lst-peso)
   (cond
     [(empty? lst-valor)
     0]
     [else
      (+ (* (first lst-valor) (first lst-peso)) (soma-ponderada (rest lst-valor) (rest lst-peso)))]
   ))
 