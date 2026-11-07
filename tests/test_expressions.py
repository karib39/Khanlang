
import unittest
from io import StringIO
from contextlib import redirect_stdout

from khan_program import run_program


class TestExpressions(unittest.TestCase):

    def test_operator_precedence(self):
        source = """
create result = 2 + 3 * 4
show result
"""

        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "14\n")

    def test_parentheses_override_precedence(self):
        source = """
create result = (2 + 3) * 4
show result
"""

        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "20\n")

    def test_subtraction_is_left_associative(self):
        source = """
create result = 20 - 5 - 3
show result
"""

        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "12\n")

    def test_nested_parentheses(self):
        source = """
create result = ((2 + 3) * (4 - 1))
show result
"""
        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "15\n")

    def test_unary_minus(self):
        source = """
create result = -5 + 8
show result
"""
        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "3\n")

    def test_function_call_inside_expression(self):
        source = """
func double(value) {
    return value * 2
}
create result = double(5) + 3
show result
"""
        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "13\n")

    def test_division_and_multiplication(self):
        source = """
create result = 18 / 3 * 2
show result
"""
        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "12.0\n")


if __name__ == "__main__":
    unittest.main()
