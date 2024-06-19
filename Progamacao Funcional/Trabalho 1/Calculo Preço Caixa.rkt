#lang racket
(require examples)

;; A função deve receber internas de uma caixa de madeira em cm, e o preço do cm dessa madeira
;; horário final, e retornar o preço final que cada caixa deve ser vendida.

;; Na hora de calcular o preço de custo da madeira, vamos adicionar 1cm para cada uma das medidas
;; dessa maneira, a caixa vai ter as medidas internas corretas. Junto ao preço de custo das madeiras, deve ser cobrado 40% a mais,
;; Valor esse que representa o custo da mão de obra.

;; base largura altura preço -> float

(examples
 (check-equal? (calcula-valor 20 15 10 0.10) 161.0)
 (check-equal? (calcula-valor 10 10 10 0.80) 677.6)
 (check-equal? (calcula-valor 40 50 60 0.10) 1864.1))

(define (calcula-areat medida-base medida-largura medida-altura)
    (+ (* (+ medida-base 1) (+ medida-largura 1))
       (* (+ medida-base 1) (+ medida-altura 1) 2)
       (* (+ medida-largura 1) (+ medida-altura 1) 2)))

(define (calcula-valor medida-base medida-largura medida-altura preco-cm)
    
    (+ (* (calcula-areat medida-base medida-largura medida-altura) preco-cm)  
    (* (calcula-areat medida-base medida-largura medida-altura) preco-cm 0.40))) 



(calcula-valor 40 50 60 0.10) 
