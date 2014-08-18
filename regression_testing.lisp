#!./interpreter.py
(require "unittest.lisp")

; Some simple sanity tests
(shouldEqual 4 (+ 1 3) "Adding two numbers")
(shouldEqual 4 (car (list 4 3 2)) "Taking the head of a list")
(shouldEqual (list 3 2) (cdr (list 4 3 2)) "Taking the tail of a list")

; Some lambda test
(set! increment (lambda (x) (+ x 1)))
(shouldEqual (increment 3) 4 "Simple incrementer lambda")

; Boolean constants
(should #t "Boolean true should be true")
(should (not #f) "Boolean false should be false")

(testEnd)
