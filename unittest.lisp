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


