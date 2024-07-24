#lang racket
(require examples)

;; Estrutura de um nó de uma arvore binparia
;; dado é o valor que será armazenado na árvore
;; sub-arv-esq é um no raiz de uma árvore ou empty
;; sub-arv-dir é um no raiz de uma árvore ou empty

(struct no (dado sub-arv-esq sub-arv-dir) #:transparent)

(define t1 (no 10 empty empty))
(define t4 (no 3 empty empty))
(define t3 (no 8 empty empty))

(define t2(no 9 t1 empty))
(define t5(no 7 t3 t2))
(define t6(no 4 t4 empty))

(define t7(no 3 t6 t5))

;; Função que soma todos os nós de uma arvore t
;; ArvoreBinaria -> número

(examples
 (check-equal? (soma-arvore t6) 7)
 (check-equal? (soma-arvore t2) 19)
 (check-equal? (soma-arvore t3) 8)
 (check-equal? (soma-arvore t7) 44)
 (check-equal? (soma-arvore empty) 0))

(define (soma-arvore t)
  (cond
    [(empty? t)
     0]
    [else
     (+ (no-dado t)
        (soma-arvore (no-sub-arv-esq t))
        (soma-arvore (no-sub-arv-dir t)))]))

;;Função que recebe uma ÁrvoreBinária t e retorna a string
;;do seu passeio pré-ordem

;;Árvore-Binária -> String
(define (string-pre-ordem t)
  (cond
    [(empty? t) ""]
    [else
     (string-append (number->string (no-dado t)) " "
                    (string-pre-ordem (no-sub-arv-esq t))
                    (string-pre-ordem (no-sub-arv-dir t)))]))

;; Função  que recebe uma ÁrvoreBinária t e retorna a string
;; do seu passeio em-ordem

(define (string-em-ordem t)
  (cond
    [(empty? t) ""]
    [else
     (string-append (string-em-ordem (no-sub-arv-esq t))
                    (number->string (no-dado t)) " "
                    (string-em-ordem (no-sub-arv-dir t)))]))
