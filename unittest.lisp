#!./interpreter.py

(set! testsFailed 0)
(set! testsSuccess 0)

(set! should
  (lambda (assertion msg)
    (if assertion
      (begin
        (set! testsSuccess (+ testsSuccess 1))
        (display ".")
        )
      (begin
        (displayln (+ "Test failed : " msg))
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
    (begin
      (displayln "")
      (if (= testsFailed 0)
        (displayln "All tests ok")
        (displayln "Some tests failed")
        )
      )
    )
  )


