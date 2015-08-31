lis.py
======

My attempt at implementing LISP in Python. It doesn't support tail call
recursion, which makes it useless for about anything practical, but was still
fun to make.

## Minimal example

```python
import lispy

PROG = """
(displayln "Hello World!")
(displayln msg)
"""

# Parse program
prog = lispy.create_prog(PROG)

# Create environnment with basic functions
env = lispy.create_base_env()

# Put the message in the environment
env['msg'] = "Hello from Python"

# Runs the code
lispy.eval_prog(prog, env)
```

## Running tests

```
python3 -m unittest discover
```

