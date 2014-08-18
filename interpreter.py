#!/usr/bin/env python3

from lispy import *
import sys

def run_file(path, env):
    with open(path) as f:
        content = f.read().splitlines()

    # Allows usage as scripts
    if content[0].startswith("#!"):
        content = content[1:]

    prog = create_prog("\n".join(content))
    eval_prog(prog, env)


def main():
    env = create_base_env()

    env['require'] = lambda s: run_file(s, env)

    if len(sys.argv) > 1:
        run_file(sys.argv[1], env)

    else:
        while True:
            prog = input_expression()
            prog = create_prog(prog)
            result = eval_prog(prog, env)

            if result is not None:
                print("=> {}".format(result))

if __name__ == "__main__":
    main()


