#!./interpreter.py

(set! testsFailed 0)
(set! testsSuccess 0)

(set! should
  (lambda (assertion msg)
    (if assertion
      (set! testsSuccess (+ testsSuccess 1))
      (begin
        (display (+ "Test failed : " msg))
        (set! testsFailed (+ testsFailed 1))
        )
      )
    )
  )

(set! shouldEqual
  (lambda (a b msg)
    (should (= a b) msg)
    )
  )

(set! testEnd
  (lambda ()
    (if (= testsFailed 0)
      (display "All tests ok")
      (display "Some tests failed")
      )
    )
  )

; Some simple sanity tests
(shouldEqual 4 (+ 1 3) "Adding two numbers")
(shouldEqual 4 (car (list 4 3 2)) "Taking the head of a list")
(shouldEqual (list 4 3 2) (cdr (list 4 3 2)) "Taking the head of a list")

(testEnd)


