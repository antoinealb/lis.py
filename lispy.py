#!/usr/bin/env python3
class LispSyntaxError(RuntimeError):
    """
    Exception raised when a Lisp syntax error is met.
    """
    pass

class LispRuntimeError(RuntimeError):
    pass

class LispMissingParameterError(LispRuntimeError):
    """
    Raised when there miss a parameter to a lambda call.
    """
    pass

class Identifier(str):
    """
    Class used to differentiate identifiers and keywords from strings.
    """

class Environment(dict):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)

        scope = self.find(key)

        if scope is None:
            raise LispRuntimeError('Unknown identifier : {}'.format(key))

        return scope[key]

    def __setitem__(self, key, val):
        scope = self.find(key)

        if scope == self:
            super().__setitem__(key, val)
        elif scope == None:
            super().__setitem__(key, val)
        else:
            scope[key] = val


    def find(self, key):
        if key in self:
            return self

        if self.parent is not None:
            return self.parent.find(key)

        return None

def create_base_env():
    env = Environment()

    # Support for basic boolean operators
    for op in ['+', '-', '*', '/', '%', '<', '>', '<=', '>=', 'and', 'or']:
        env[op] = eval('lambda x, y: x {} y'.format(op))

    env['='] = lambda x, y: x == y

    # Boolean constants
    env['#t'] = True
    env['#f'] = False
    env['not'] = lambda b: not b

    # List operations
    env['list'] = lambda *args: list(args)
    env['car'] = lambda l: l[0]
    env['cdr'] = lambda l: l[1:]
    env['len'] = len

    env['display'] = lambda l: print(l, end='')
    env['displayln'] = lambda l: print(l)

    return env

def atom(string):
    """
    Creates an Atom from a string.
    """
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return Identifier(string)

def tokenize(prog):
    """
    Cuts a program into a list of list of atoms.
    """
    def inner_parser(prog):
        result = []
        while len(prog) > 0:
            val = prog.pop(0)

            if val == '(':
                result.append(inner_parser(prog))

            elif val == ')':
                return result

            elif val.startswith('"'):
                while not val.endswith('"'):
                    val = val + " " + prog.pop(0)
                result.append(val[1:-1])

            else:
                result.append(atom(val))

        # If we reach here, it means we have a non terminated list.
        raise LispSyntaxError('Non terminated list')

    # Converts the string into a flat list
    prog = prog.replace("(", " ( ").replace(")", " ) ").split()
    prog.pop(0) # Drops the initial '('
    return inner_parser(prog)

def create_prog(prog_content):
    """
    This function creates a program from the given content by preprocessing it.
    It starts by wrapping the whole program in a begin expression
    """
    prog_content = prog_content.splitlines()
    prog_content = [l for l in prog_content if not l.lstrip().startswith(";")]
    prog_content = "\n".join(prog_content)
    prog_content = "(begin {})".format(prog_content)
    return tokenize(prog_content)

def eval_prog(prog, env=None):

    if env is None:
        env = Environment()

    if isinstance(prog, int) or isinstance(prog, float):
        return prog

    if isinstance(prog, Identifier):
        return env[prog]

    # String literals
    if isinstance(prog, str):
        return prog

    if prog[0] == 'set!':
        varname = prog[1]
        varvalue = eval_prog(prog[2], env)
        env[varname] = varvalue
        return

    if prog[0] == 'lambda':
        argument_names = prog[1]
        expression = prog[2]
        def f(*args):
            if len(args) < len(argument_names):
                raise LispMissingParameterError
            updated_env = Environment(env, zip(argument_names, args))
            return eval_prog(expression, updated_env)

        return f

    if prog[0] == 'quote':
        return prog[1]

    if prog[0] == 'begin':
        val = None
        for expr in prog[1:]:
            val = eval_prog(expr, env)

        return val

    if prog[0] == 'if':
        cond = eval_prog(prog[1], env)
        if cond:
            return eval_prog(prog[2], env)
        else:
            return eval_prog(prog[3], env)

    # If we get there it means that we have a function call
    args = [eval_prog(v, env) for v in prog]
    func = args.pop(0)

    return func(*args)

def input_expression():
    """
    Allows the user to input a multi line expression.
    """
    level = 0

    s = input(">>> ")
    level += s.count('(')
    level -= s.count(')')

    result = [s]

    while level:
        prompt = "... " + "  " * level
        s = input(prompt)
        level += s.count('(')
        level -= s.count(')')
        result.append(s)

    return ' '.join(result)

