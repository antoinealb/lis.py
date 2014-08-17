#!/usr/bin/env python3

from lispy import *
import sys

def main():
    env = create_base_env()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            prog = create_prog(f.read())

        eval_prog(prog, env)

    else:
        while True:
            prog = input_expression()
            prog = create_prog(prog)
            result = eval_prog(prog, env)

            if result is not None:
                print("=> {}".format(result))

if __name__ == "__main__":
    main()


