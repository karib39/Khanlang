
import unittest
from io import StringIO
from contextlib import redirect_stdout

from khan_program import run_program


class TestRuntime(unittest.TestCase):

    def test_variable_and_output(self):
        source = """
create total = 10
create result = total + 5
show result
"""

        output = StringIO()

        with redirect_stdout(output):
            environment = run_program(source)

        self.assertEqual(output.getvalue(), "15\n")
        self.assertEqual(environment["result"], 15)

    def test_function_call(self):
        source = """
func add(a, b) {
    return a + b
}

create result = add(10, 20)
show result
"""

        output = StringIO()

        with redirect_stdout(output):
            environment = run_program(source)

        self.assertEqual(output.getvalue(), "30\n")
        self.assertEqual(environment["result"], 30)

    def test_if_else(self):
        source = """
create age = 20

if age >= 18 {
    show "Adult"
} else {
    show "Minor"
}
"""

        output = StringIO()

        with redirect_stdout(output):
            run_program(source)

        self.assertEqual(output.getvalue(), "Adult\n")

    def test_while_loop(self):
        source = """
create count = 1

while count <= 3 {
    show count
    create count = count + 1
}
"""

        output = StringIO()

        with redirect_stdout(output):
            environment = run_program(source)

        self.assertEqual(output.getvalue(), "1\n2\n3\n")
        self.assertEqual(environment["count"], 4)


if __name__ == "__main__":
    unittest.main()
