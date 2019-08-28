(define (factorial n k)
  (if (zero? n)
      k
      (factorial (- n 1) (* k n))
      ) ; End of if statement
  ) ; End of factorial definition