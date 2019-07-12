;; Extra Scheme Questions ;;


; Q5
(define lst
  (cons
    (cons 1 nil) ; car
    (cons 2 
      (cons
        (cons 3 4)
        (cons 5 nil)
      )
    )
  )
)

; Q6
(define (composed f g)
  (lambda (x) (f (g x)))
)

; Q7
(define (remove item lst)
  (filter ; call the filter function
    (lambda (x) 
      (not (= item x)))
    lst
  )
)


;;; Tests
(remove 3 nil)
; expect ()
(remove 3 '(1 3 5))
; expect (1 5)
(remove 5 '(5 3 5 5 1 4 5 4))
; expect (3 1 4 4)

; Q8
(define (no-repeats s)
  (if (null? s) s 
    (cons (car s)
      (no-repeats
        (filter
          (lambda (x) (not (= (car s) x)))
          (cdr s)
        ) ; End of filter
      ) ; End of no-repeats
    ) ; End of cons
  ) ; End of if suite
)

; Q9
(define (substitute s old new)
  (cond
    ((null? s) s) ; If s is empty, then just return s
    ; if 'car s' is a nested list, then construct a list where the first is the recursive call of substitute on car s,
    ; while the .rest is the recursive call of substitute on cdr s
    ((pair? (car s)) (cons
                      (substitute (car s) old new)
                      (substitute (cdr s) old new)
    ))
    ; If 'car s' is old, start constructing a list where '.first' is 'new' while '.rest' is the
    ; recursive call of substitute on cdr s
    ((eq? (car s) old) (cons new (substitute (cdr s) old new)))
    ; Otherwise, if (car s) is just an element that is not 'old', construct a list where the '.first' is still 'car s',
    ; and '.rest' is the recursive call of substitute on 'cdr s'
    (else (cons (car s) (substitute (cdr s) old new)))
  )
)

; Q10
(define (sub-all s olds news)
  (if (null? olds)
    s
    (sub-all
      (substitute s (car olds) (car news))
      (cdr olds)
      (cdr news)
    ) ; End of sub-all
  ); End of if 
) ; End of procedure definition