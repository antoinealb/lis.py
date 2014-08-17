#!/usr/bin/env python3

import unittest
from unittest.mock import *
from lispy import *

class AtomTestCase(unittest.TestCase):
    def test_int_atom(self):
        """ Checks that creating an int atom works. """
        self.assertEqual(atom('3'), 3)
        self.assertEqual(atom('5'), 5)

    def test_float_atom(self):
        """
        Checks that we can create an atom from a float.
        """
        self.assertEqual(atom('4.2'), 4.2)
        self.assertEqual(atom('5.2'), 5.2)

    def test_string_atom(self):
        """
        Checks if we can create an atom from a string.
        """
        self.assertEqual(atom('foo'), 'foo')

class TokenizerTestCase(unittest.TestCase):
    def test_simple_list(self):
        """
        Tests if a simple list works.
        """
        prog = "(12)"
        self.assertEqual([12], tokenize(prog))

    def test_list_with_many_elements(self):
        """
        Checks if a list with many elements works too.
        """
        prog = "(1 2 3)"
        self.assertEqual([1,2,3], tokenize(prog))

    def test_nested_list(self):
        """
        Checks if a list works with nested lists.
        """
        prog = '((1 2 3))'
        self.assertEqual([[1,2,3]], tokenize(prog))

    def test_can_mix_lists_and_atoms(self):
        """
        Checks if we can mix nested lists and atoms.
        """
        prog = '(1 (foo bar) 2 3 (4 5))'
        expected = [1, ['foo', 'bar'], 2, 3, [4, 5]]
        self.assertEqual(expected, tokenize(prog))

    def test_unfinished_list_raises_error(self):
        """
        Checks if a non terminated list raises the correct exception.
        """
        prog = '(1 2' # list not terminated
        with self.assertRaises(LispSyntaxError):
            tokenize(prog)

class EnvironmentTestCase(unittest.TestCase):

    def test_env_find_variable(self):
        env = Environment()
        env['foo'] = 12
        self.assertEqual(12, env['foo'])

    def test_env_nested(self):
        """
        Checks that we can find variables in nested environment.
        """
        parent = Environment()
        parent['foo'] = 12
        child = Environment(parent=parent)
        self.assertEqual(12, child['foo'])

    def test_not_found_raises_error(self):
        """
        Checks that not having the correct key raises a LispError.
        """
        env = Environment()
        with self.assertRaises(LispRuntimeError):
            env['foo']

    def test_can_create_dict_like_object(self):
        """
        Checks that we can create an environment as a dictionnary.
        """
        a = dict(foo=42)
        self.assertEqual(a['foo'], 42)
        e = Environment(foo=42)
        self.assertEqual(e['foo'], 42)

    def test_find(self):
        """
        Checks the find method which is used to find the smallest environment
        which contains a var.
        """
        parent = Environment(foo=42)
        self.assertEqual(parent, parent.find('foo'))

        child = Environment(parent)
        self.assertEqual(parent, child.find('foo'))
        self.assertEqual(None, child.find('bar'))

    def test_find_nested(self):
        parent = Environment(foo=42)
        child = Environment(parent=parent)
        child2 = Environment(parent=child)

        self.assertEqual(parent, child.find('foo'))
        self.assertEqual(parent, child2.find('foo'))

    def test_can_set_var_from_parent(self):
        parent = Environment(foo=10)
        child = Environment(parent)
        child['foo'] = 42
        self.assertEqual(child['foo'], 42)
        self.assertEqual(parent['foo'], 42)

    def test_can_get_var_from_very_nested(self):
        parent = Environment(foo=10)
        child = Environment(Environment(parent))
        self.assertEqual(parent['foo'], 10)
        self.assertEqual(child['foo'], 10)

    def test_can_use_in_construct(self):
        parent = Environment(foo=10)
        self.assertIn('foo', parent)

class EnvironmentFactoryTestCase(unittest.TestCase):
    """
    Tests for the environment factory which produces base constructs.
    """
    def setUp(self):
        self.env = create_base_env()

    def test_environment_factory(self):
        self.assertIsInstance(self.env, Environment)

    def test_operators(self):
        """
        Checks that basic math operator works correctly.
        """
        self.assertEqual(self.env['+'](2,3), 5)
        self.assertEqual(self.env['-'](2,3), -1)
        self.assertEqual(self.env['*'](2,3), 6)
        self.assertEqual(self.env['/'](3,2), 1.5)
        self.assertEqual(self.env['%'](3,2), 1)

    def test_boolean(self):
        """
        Checks that boolean operators works.
        """
        self.assertFalse(self.env['<'](3,2))
        self.assertTrue(self.env['>'](3,2))
        self.assertTrue(self.env['>='](3,3))
        self.assertFalse(self.env['<='](3,2))
        self.assertTrue(self.env['='](3,3))
        self.assertTrue(self.env['and'](True, True))
        self.assertTrue(self.env['or'](True, False))

    def test_list_operations(self):
        """
        Checks that list operations works properly.
        """
        self.assertEqual(self.env['list'](1,2,3), [1,2,3])
        self.assertEqual(self.env['car']([1,2,3]), 1)
        self.assertEqual(self.env['cdr']([1,2,3]), [2,3])
        self.assertEqual(self.env['len']([1,2,3]), 3)

    @patch('lispy.print', create=True)
    def test_io(self, print_mock):
        """
        Tests IO operations.
        """
        self.env['display'](12)
        print_mock.assert_called_once_with(12)


class EvalTestCase(unittest.TestCase):
    def test_eval_litterals(self):
        self.assertEqual(lisp_eval(3), 3)
        self.assertEqual(lisp_eval(3.2), 3.2)

    def test_set_variable(self):
        """
        Checks that setting a variable returns an updated Environment.
        """
        env = Environment()
        lisp_eval(['set!', 'foo', 42], env)
        self.assertEqual(env['foo'], 42)

    def test_set_variable_empty_env(self):
        """
        Checks that we can set a value even if no environment is provided.
        """
        lisp_eval(['set!', 'foo', 42])

    def test_get_variable(self):
        """
        Checks that we can set then get a variable.
        """
        env = Environment(foo=42)
        result = lisp_eval('foo', env)
        self.assertEqual(result, 42)

    def test_if_true(self):
        """
        Checks that the true condition of the if is taken correctly.
        """
        prog = ['if', 1, 42, 0]
        result = lisp_eval(prog)
        self.assertEqual(result, 42)

    def test_if_false(self):
        """
        Checks that the false branch of the if works too.
        """
        prog = ['if', 0, 42, 0]
        result = lisp_eval(prog)
        self.assertEqual(result, 0)

    def test_if_condition_needs_evaluation(self):
        """
        Checks that a real condition (aka something that needs to be evaluated)
        works too.
        """
        env = Environment(cond=0)
        prog = ['if', 'cond', 1, 0]
        result = lisp_eval(prog, env)
        self.assertEqual(result, 0)

    def test_if_condition_values_works_too(self):
        """
        Checks that the value are interpreted too.
        """
        env = Environment(foo=42, bar=84)

        prog = ['if', 1, 'foo', 'bar']
        result = lisp_eval(prog, env)
        self.assertEqual(result, 42)

        prog = ['if', 0, 'foo', 'bar']
        result = lisp_eval(prog, env)
        self.assertEqual(result, 84)

    def test_call(self):
        """
        Checks that function call works too.
        """
        env = Environment()
        env['f'] = lambda x: x**2
        prog = ['f', 3]
        self.assertEqual(lisp_eval(prog, env), 9)

    def test_can_create_lambda(self):
        """
        Checks if we can create a simple lambda.
        """
        prog = ['lambda', ['x'], 'x']
        f = lisp_eval(prog)
        self.assertEqual(3, f(3))

    def test_more_complicated_lambda(self):
        """
        Checks if a lambda involving another lambda works.
        """
        env = Environment()
        env['+'] = lambda x,y:x+y # simple add operator
        prog = ['lambda', ['x', 'y'], ['+', 'x', 'y']]
        f = lisp_eval(prog, env)
        self.assertEqual(5, f(3, 2))

    def test_begin(self):
        """
        Checks if the begin instruction works correctly.
        """
        env = Environment()
        env['foo'] = MagicMock(name='foo')

        prog = ['begin', ['foo', 1], 42]

        val = lisp_eval(prog, env)

        env['foo'].assert_called_once_with(1)
        self.assertEqual(val, 42)

    def test_empty_begin_doesnt_crash(self):
        """
        Checks that an empty begin statement doesn't crash but raises a syntax
        error.
        """
        prog = ['begin']
        self.assertIsNone(lisp_eval(prog))

    def test_missing_parameter(self):
        """
        Checks if the correct syntax error is raised when missing a parameter
        in a lambda.
        """
        env = Environment()
        prog = [['lambda', ['x', 'y'], 'x'], 3]

        with self.assertRaises(LispMissingParameterError):
            lisp_eval(prog, env)


class IntegrationTesting(unittest.TestCase):
    """
    Checks that everything works together.
    """
    def test_simple_program(self):
        """
        Checks if a simple program works.
        """
        env = create_base_env()
        prog1 = tokenize('(set! double (lambda (x) (+ x x)))')
        prog2 = tokenize('(double 3)')
        lisp_eval(prog1, env)
        result = lisp_eval(prog2, env)
        self.assertEqual(6, result)

    def test_can_create_whole_program(self):
        """
        Checks that we can create a real life program, with newlines and stuff.
        """
        prog_content = """
        (set! x 3)
        (set! y 4)
        """
        prog = create_prog(prog_content)
        expected = ['begin', ['set!', 'x', 3], ['set!', 'y', 4]]
        self.assertEqual(prog, expected)

    def test_end_to_end_program(self):
        """
        Checks that a complete parsing + evaluation chain works.
        """
        prog_content = """
        (set! x 3)
        (set! adder (lambda (y) (+ x y)))
        (set! result (adder 2))
        """
        prog = create_prog(prog_content)
        env = create_base_env()
        lisp_eval(prog, env)
        self.assertEqual(env['result'], 5)

    def test_recursion(self):
        """
        Checks that recursion works by using a recursive version of factorial.
        """
        prog = """
        (set! factorial
          (lambda (x)
            (if x
              (* x (factorial (- x 1)))
              1
              )
            )
          )

        (factorial 5)"""
        prog = create_prog(prog)

        env = create_base_env()
        val = lisp_eval(prog, env)
        self.assertEqual(val, 120)

    def test_multiple_assignment(self):
        prog = """
        (set! a 12)
        (set! b 13)
        """
        prog = create_prog(prog)
        env = create_base_env()
        lisp_eval(prog, env)

        k = env.keys()

        self.assertIn('a', k)
        self.assertIn('b', k)

    def test_comments(self):
        prog = """
        ; This is a comment
        (set! a 12)
        """
        prog = create_prog(prog)
        expected = ['begin', ['set!', 'a', 12]]
        self.assertEqual(prog, expected)

    @patch('lispy.input', create=True)
    def test_input_trivial_expression(self, input_mock):
        input_mock.side_effect = ['2']
        self.assertEqual('2', input_expression())

    @patch('lispy.input', create=True)
    def test_input_real_expression(self, input_mock):
        s = '(set! bar (list 1 2 3))'
        input_mock.side_effect = [s]
        self.assertEqual(s, input_expression())

    @patch('lispy.input', create=True)
    def test_multiline_expression(self, input_mock):
        input_mock.side_effect = ['(set! bar', '1', ')']
        self.assertEqual('(set! bar 1 )', input_expression())

if __name__ == '__main__':
    unittest.main()
