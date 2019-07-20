(define (reverse lst)
    'YOUR-CODE-HERE
    (if (null? lst)
      ()
      (append (reverse (cdr lst)) (list (car lst)))
    ) ; End of if
) ; End of define

(define (longest-increasing-subsequence lst)
    'YOUR-CODE-HERE
    (if (null? lst)
      lst
      (begin
        (define with-car
          (cons
            (car lst)
            (longest-increasing-subsequence
              (filter
                (lambda (x) (> x (car lst)))
                (cdr lst)))))
        (define without-car
          (longest-increasing-subsequence (cdr lst)))
        (if (> (length with-car) (length without-car))
          with-car
          without-car)
      ) ; End of begin
    ) ; End of if
)

(define (cadr s) (car (cdr s)))
(define (caddr s) (cadr (cdr s)))


; derive returns the derivative of EXPR with respect to VAR
(define (derive expr var)
  (cond ((number? expr) 0)
        ((variable? expr) (if (same-variable? expr var) 1 0))
        ((sum? expr) (derive-sum expr var))
        ((product? expr) (derive-product expr var))
        ((exp? expr) (derive-exp expr var))
        (else 'Error)))

; Variables are represented as symbols
(define (variable? x) (symbol? x))
(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

; Numbers are compared with =
(define (=number? expr num)
  (and (number? expr) (= expr num)))

; Sums are represented as lists that start with +.
(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list '+ a1 a2))))
(define (sum? x)
  (and (list? x) (eq? (car x) '+)))
(define (addend s) (cadr s))
(define (augend s) (caddr s))

; Products are represented as lists that start with *.
(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list '* m1 m2))))
(define (product? x)
  (and (list? x) (eq? (car x) '*)))
(define (multiplier p) (cadr p))
(define (multiplicand p) (caddr p))

(define (derive-sum expr var)
  (make-sum
    (derive (addend expr) var)
    (derive (augend expr) var)
  ) ; End of make-sum
) ; End of define

(define (derive-product expr var)
  (begin
    (define dmul (derive (multiplier expr) var))
    (define dcand (derive (multiplicand expr) var)))
  (make-sum
    (make-product dmul (multiplicand expr))
    (make-product (multiplier expr) dcand)
  ); End of make-sum
) ; End of define

; Exponentiations are represented as lists that start with ^.
(define (make-exp base exponent)
  (cond
    ((= exponent 0) 1)
    ((= exponent 1) base)
    ((number? base) (expt base exponent))
    (else (list '^ base exponent))
  ) ; End of cond
) ; End of define

(define (base exp)
  (cadr exp)
)

(define (exponent exp)
  (caddr exp)
)

(define (exp? exp)
  (and
    (list? exp)
    (eq? (car exp) '^))
)

(define x^2 (make-exp 'x 2))
(define x^3 (make-exp 'x 3))

(define (derive-exp exp var)
  (if (= 2 (exponent exp))
    (make-product (exponent exp) (base exp))
    (make-product (exponent exp) (make-exp (base exp) (- (exponent exp) 1)))
  ) ; End of if
) ; End of define