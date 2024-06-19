#lang racket
(require examples)

;; Receber três números, entrega a diferença entre o maior e o menor
(define (diferenca x y)
  (abs (- x y)))

;; Recebe horário de início de um evento e o horário de termino do mesmo, devolvendo a duração total deste evento em minutos.
(examples
 (check-equal? (duracao-evento 15 30 19 00) 210)
  (check-equal? (duracao-evento 23 40 2 30) 170)
  (check-equal? (duracao-evento 15 30 17 00) 90)
  (check-equal? (duracao-evento 23 00 23 30) 30)
  (check-equal? (duracao-evento 15 30 15 30) 0)
  (check-equal? (duracao-evento 22 50 23 30) 40))
  
(define (duracao-evento hora-ini minuto-ini hora-fim minuto-fim)
  (cond
    [(= hora-ini hora-fim)
     (cond
       [(<= minuto-ini minuto-fim)
        (- minuto-fim minuto-ini)]
       [(> minuto-ini minuto-fim)
        (- (+ (+ minuto-fim 60) (converteh (+ hora-fim 24 -1)))
           (+ minuto-ini (converteh hora-ini)))])]
    [(< hora-ini hora-fim)
     (cond
       [(<= minuto-ini minuto-fim)
        (+ (converteh (- hora-fim hora-ini)) (- minuto-fim minuto-ini))]
       [(> minuto-ini minuto-fim)
        (+ (converteh (- hora-fim 1 hora-ini))
           (- (+ minuto-fim 60) minuto-ini))])]
    [(> hora-ini hora-fim)
     (cond
       [(<= minuto-ini minuto-fim)
        (+ (converteh (- (+ hora-fim 24) hora-ini))
           (- minuto-fim minuto-ini))]
       [(> minuto-ini minuto-fim)
        (+ (converteh (- (+ hora-fim 24) 1 hora-ini))
           (- (+ 60 minuto-fim) minuto-ini))])]))

(define (converteh horas)
   (* horas 60))
       
;; Recebe um número com 3 digitos e devolve ele na ordem inversa
(define (inverter-numero n)
  (define digito-1 (remainder n 10))
  (define digito-2 (remainder (quotient n 10) 10))
  (define digito-3 (quotient n 100))
  (+ (* digito-1 100) (* digito-2 10) digito-3))

