;; Scheme ;;

; Q3
(define (over-or-under x y)
  'YOUR-CODE-HERE
  (cond
   ((< x y) -1)
   ((> x y) 1)
   (else 0))
)

;;; Tests
(over-or-under 1 2)
; expect -1
(over-or-under 2 1)
; expect 1
(over-or-under 1 1)
; expect 0

; Q4
(define (filter f lst)
  (cond
  ; Base case: if lst is empty, then just return an empty list
  ((null? lst) ())
  ; Recursive case: If appyling f on the first element of lst returns true,
  ; construct a list with cons using (car lst) as first and (filter f (cdr lst)) as rest
  ( (f (car lst)) (cons (car lst) (filter f (cdr lst))))
  ; Otherwise, check for the result of applying f to the next element of lst
  (else (filter f (cdr lst)))
  )
)

;;; Tests
(define (even? x)
  (= (modulo x 2) 0))
(filter even? '(0 1 1 2 3 5 8))
; expect (0 2 8)

; Q5
(define (make-adder num)
  (lambda (x) (+ num x))
)

;;; Tests
(define adder (make-adder 5))
(adder 8)
; expect 13