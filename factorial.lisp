#!./interpreter.py

(require "unittest.lisp")

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

(shouldEqual (factorial 1) 1 "Factorial of one should be one")
(shouldEqual (factorial 5) 120 "5! = 120")

(testEnd)
