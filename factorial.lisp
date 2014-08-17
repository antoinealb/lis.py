; This little example program computes the factorial of a number using a
; recursive approach.
(set! factorial
  (lambda (x)
    (if (> x 1)
      (* x (factorial (- x 1)))
      1
      )
    )
  )

; Should display 120
(display (factorial 5))
