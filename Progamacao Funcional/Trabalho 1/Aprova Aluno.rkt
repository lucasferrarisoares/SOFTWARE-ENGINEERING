#lang racket
(require examples)

;; Recebe as quatro notas do aluno e a média esperada
;; verifica se o aluno foi aprovado pelo requisito média

(examples
 (check-equal? (aprovanota 6 6 6 6 5) #t)
 (check-equal? (aprovanota 5 8 2 9 5) #t)
 (check-equal? (aprovanota 4 5 6 5 6) #f))

(define (aprovanota nota1 nota2 nota3 nota4 media)
  (define mediaaluno (/ (+ nota1 nota2 nota3 nota4) 4))
  (>= mediaaluno media))

(examples
 (check-equal? (calcpresente 5 25 0.2) #t)
 (check-equal? (calcpresente 2 10 0.1) #f)
 (check-equal? (calcpresente 6 10 0.7) #t))

;; Recebe as faltas do aluno, CH total de aula, e a porcentagem tolerada de faltas
;; Devolve se o aluno está ou não está aprovado pelo quisito presença

(define (calcpresente faltas CH percentual)
  (define limite (* CH percentual))
  (<= faltas limite))

;; Recebe o dados de um aluno, carga horária de uma disiplina e percentual de faltas permitidas, além da média da matéria
;; Calcula se o aluno atingiu a média de nota, e se as faltas estão dentro do permitido
;; Diz se o aluno foi aprovado ou não.
(struct aluno (RA Nome N1 N2 N3 N4 FALTAS) #:transparent)

(define aluno1 (aluno 123 "João" 6 6 6 6 5))
(define aluno2 (aluno 124 "Maria" 5 8 2 9 5))
(define aluno3 (aluno 125 "Pedro" 4 5 6 5 6))

(examples
 (check-equal? (aprovaaluno aluno1 5 25 0.2) "João foi aprovado!")
 (check-equal? (aprovaaluno aluno2 5 10 0.1) "Maria não atingiu a presença necessária!")
 (check-equal? (aprovaaluno aluno3 6 10 0.7) "Pedro não obteve a média necessária!"))

(define (aprovaaluno aluno media CH percentual)
  (define nota (aprovanota (aluno-N1 aluno) (aluno-N2 aluno) (aluno-N3 aluno) (aluno-N4 aluno) media))
  (define presenca (calcpresente (aluno-FALTAS aluno) CH percentual))
  (cond
    [(and nota presenca) (string-append (aluno-Nome aluno) " foi aprovado!")]
    [(not nota) (string-append (aluno-Nome aluno) " não obteve a média necessária!")]
    [else (string-append (aluno-Nome aluno) " não atingiu a presença necessária!")]))

