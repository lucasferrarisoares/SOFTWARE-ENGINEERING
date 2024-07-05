#lang racket
(require examples)


(examples
 (check-equal? (junta-virgula-e (list "pão" "queijo" "leite" "presunto" "achocolatado"))
               "pão, queijo, leite, presunto e achocolatado")
 (check-equal? (junta-virgula-e (list "maçã" "laranja" "abacaxi"))
               "maçã, laranja e abacaxi")
 (check-equal? (junta-virgula-e (list "coca" "chocolate"))
               "coca e chocolate")
 (check-equal? (junta-virgula-e (list ))
               "")
 (check-equal? (junta-virgula-e (list "pringles"))
               "pringles"))


;;Recebe uma lista com strings e devolve uma única string com todos os elementos da lista.
;;Para lista única, vai ser somente o elemento
;;Em caso de listas com dois elemntos, sera "elemento 1 e elementos 2"
;;Para 3 ou mais elementos, "elemento 1, elemento2 e elemento3" e assim por diante
;;listaDeStrings --> String

 
 (define (junta-virgula-e lst)
  ;;Define os casos base, lista vazia;
  ;;Único elemento;
  ;;Dois elementos;
  (cond
    [(empty? lst)
     ""]
    [(empty? (rest lst))
     (first lst)]
    [(empty? (rest (rest lst)))
     (string-append (first lst) " e " (first (rest lst)))]
    [else
     (string-append (first lst) ", " (junta-virgula-e (rest lst)))]))