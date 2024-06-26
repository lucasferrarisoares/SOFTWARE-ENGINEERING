#lang racket
(require examples)
(examples
 (check-equal? (detecta-palindromo 1221) #t)
  (check-equal? (detecta-palindromo 1352) #f)
  (check-equal? (detecta-palindromo 2020) #f)
  (check-equal? (detecta-palindromo 9889) #t)
  (check-equal? (detecta-palindromo 1111) #t)
  (check-equal? (detecta-palindromo 4242) #f))

;; Recebe um número com 4 digitos e detecta se ele é um palindromo ou não;;
(define (detecta-palindromo n)
  (define digito-1 (remainder n 10))
  (define digito-2 (remainder (quotient n 10) 10))
  (define digito-3 (remainder (quotient n 100) 10))
  (define digito-4 (quotient n 1000))
  (define ninverso (+ (* digito-1 1000) (* digito-2 100) (* digito-3 10) digito-4))
  (if (equal? n ninverso)
      #t
      #f))
 
    
