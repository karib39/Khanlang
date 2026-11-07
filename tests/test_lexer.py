
import unittest
from khan_lexer import tokenize


class TestLexer(unittest.TestCase):

    def test_create_statement(self):
        tokens = tokenize("create age = 20")

        self.assertEqual(tokens[0].value, "create")
        self.assertEqual(tokens[1].value, "age")
        self.assertEqual(tokens[2].value, "=")
        self.assertEqual(tokens[3].value, 20)

    def test_arithmetic_expression(self):
        tokens = tokenize("10 + 5 * 2")

        self.assertEqual(
            [token.value for token in tokens],
            [10, "+", 5, "*", 2]
        )

    def test_comparison_operators(self):
        tokens = tokenize("== != >= <= > <")

        self.assertEqual(
            [token.value for token in tokens],
            ["==", "!=", ">=", "<=", ">", "<"]
        )

    def test_braces_and_punctuation(self):
        tokens = tokenize("func add(a, b) { }")

        self.assertEqual(
            [token.value for token in tokens],
            ["func", "add", "(", "a", ",", "b", ")", "{", "}"]
        )

    def test_string_recognition(self):
        tokens = tokenize('"hello world"')

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, "STRING")


if __name__ == "__main__":
    unittest.main()
