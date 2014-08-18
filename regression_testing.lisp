#!./interpreter.py
(require "unittest.lisp")

; Some simple sanity tests
(shouldEqual 4 (+ 1 3) "Adding two numbers")
(shouldEqual 4 (car (list 4 3 2)) "Taking the head of a list")
(shouldEqual (list 3 2) (cdr (list 4 3 2)) "Taking the tail of a list")
(shouldEqual (car (quote (1 2 3))) 1 "Simple list test")
(shouldEqual (len (list 1 2 3 4)) 4 "List lenght test")
(shouldEqual (cons 1 (list 2 3)) (list 1 2 3) "List append test")

; Some lambda test
(set! increment (lambda (x) (+ x 1)))
(shouldEqual (increment 3) 4 "Simple incrementer lambda")

; Boolean constants
(should #t "Boolean true should be true")
(should (not #f) "Boolean false should be false")

(testEnd)
