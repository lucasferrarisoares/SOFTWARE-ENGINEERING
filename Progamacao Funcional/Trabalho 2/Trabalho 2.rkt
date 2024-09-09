#lang racket
(struct mensagem (emissor receptor tamanho) #:mutable)

;; ----------- FUNÇÕES AUXILIARES ---------------
;; Função map
(define (mapeia f lst)
  (cond
    [(empty? lst) empty]
    [else (cons (f (first lst)) (mapeia f (rest lst)))]))
;; Função para dividir linhas em listas de pacotes
(define (mapeialinha lst)
  (cond
    [(empty? lst) empty]
    [else (cons (string-split (first lst) " ") (mapeialinha (rest lst)))]))
;; Função para ordenar a lista de mensagens
  (define (ordena-lista lst)
    (define (quicksort lst)
      (cond
        [(empty? lst) (list )]
        [else
          (let* [(pivo (first lst))
                (menor (filter (lambda (x) (< (mensagem-tamanho x) (mensagem-tamanho pivo))) (rest lst)))
                (maior (filter (lambda (x) (>= (mensagem-tamanho x) (mensagem-tamanho pivo))) (rest lst)))]
               (append (quicksort maior) (list pivo) (quicksort menor)))]))
    (quicksort lst))
;; ----------- FUNÇÕES AUXILIARES ---------------

;; Função para processar o texto de entrada
(define (processa entrada)
  (define listalinhas (string-split entrada "\r\n"))
  (define listaespecifica (mapeialinha listalinhas))
  (define listamensagem '()) ;; Lista de mensagens

;; Função para encontrar ou criar uma mensagem com emissores e receptores em comum
(define (atualizar-mensagem emissor receptor tamanho)
  (let ([x (findf (lambda (m) (and (equal? (mensagem-emissor m) emissor)
                                   (equal? (mensagem-receptor m) receptor)))
                  listamensagem)])
    (if x
        ;; Atualiza o tamanho da mensagem existente
        (set-mensagem-tamanho! x (+ (mensagem-tamanho x) tamanho))
        ;; Adiciona uma nova mensagem à lista
        (set! listamensagem (cons (mensagem emissor receptor tamanho) listamensagem)))))

;; Processa cada pacote de dados
(for-each
 (lambda (pacote)
   (let* ([emissor (first pacote)]
          [receptor (second pacote)]
          [tamanho (string->number (third pacote))])
     (atualizar-mensagem emissor receptor tamanho)))
 listaespecifica)
  
;; Ordena os resultados
(define resultados-ordenados (ordena-lista listamensagem))
  
;; Formata a saída
(define (formata-saida mensagem)
  (format "Origem: ~a Destino: ~a Bytes transferidos: ~a\n"
          (mensagem-emissor mensagem)
          (mensagem-receptor mensagem)
          (mensagem-tamanho mensagem)))
  
;; Gera o texto de saída
(apply string-append (map formata-saida resultados-ordenados)))


;; Parser de argumentos da linha de comando
(define output-function (make-parameter "output.txt"))
(define input-function (make-parameter "input.txt"))

(define args (command-line #:program "Segundo Trabalho"
                           #:once-each
                           [("-i" "--input") if
                             "nome do arquivo de entrada (default: input.txt)"
                             (input-function if)]
                           [("-o" "--output") of
                             "nome do arquivo de saída (default: output.txt)"
                             (output-function of)]
                           #:args ()
                           (list (input-function) (output-function) )))

(define arg-lst args)

(define input-file (first arg-lst))
(define output-file (second arg-lst))

;; Leitura do arquivo de entrada
(define in-port (open-input-file input-file))
(define input-text (port->string in-port))
(close-input-port in-port)

;; Criação do texto de saída
(define output-text (processa input-text))

;; Escrita do resultado no arquivo de saída
(define out-port (open-output-file output-file #:exists 'replace))
(display output-text out-port)
(close-output-port out-port)
