
import unittest

from khan_program import run_program


class TestErrorHandling(unittest.TestCase):

    def test_undefined_variable(self):
        source = """
show missing
"""

        with self.assertRaises(NameError):
            run_program(source)

    def test_division_by_zero(self):
        source = """
create result = 10 / 0
"""

        with self.assertRaises(ZeroDivisionError):
            run_program(source)

    def test_invalid_type_operation(self):
        source = """
create result = "hello" + 5
"""

        with self.assertRaises(TypeError):
            run_program(source)

    def test_invalid_assignment_syntax(self):
        source = """
create total 10
"""

        with self.assertRaises(SyntaxError):
            run_program(source)
    def test_missing_right_operand(self):
        source = """
create result = 5 +
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

    def test_missing_left_operand(self):
        source = """
create result = * 5
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

    def test_missing_division_operand(self):
        source = """
create result = 10 /
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

    def test_unclosed_parentheses(self):
        source = """
create result = (2 + 3
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

    def test_unexpected_operator(self):
        source = """
create result = 2 + * 3
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

    def test_empty_parentheses(self):
        source = """
create result = ()
"""

        with self.assertRaises(SyntaxError):
            run_program(source)

if __name__ == "__main__":
    unittest.main()
