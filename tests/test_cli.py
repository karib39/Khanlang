
import unittest
import subprocess
import sys
import tempfile

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROGRAM = PROJECT_DIR / "khan_program.py"


class TestCommandLine(unittest.TestCase):

    def run_khan(self, filename):
        return subprocess.run(
            [sys.executable, str(PROGRAM), str(filename)],
            capture_output=True,
            text=True
        )

    def test_invalid_file_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "program.txt"
            filename.write_text("show 10", encoding="utf-8")

            result = self.run_khan(filename)

            self.assertIn(
                "must use the .khan extension",
                result.stdout
            )
            self.assertEqual(result.returncode, 1)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "missing.khan"

            result = self.run_khan(filename)

            self.assertIn("not found", result.stdout)
            self.assertEqual(result.returncode, 1)

    def test_runtime_error_message(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "program.khan"
            filename.write_text("show missing", encoding="utf-8")

            result = self.run_khan(filename)

            self.assertIn("Khanlang Error:", result.stdout)
            self.assertIn("missing", result.stdout)
            self.assertEqual(result.returncode, 1)

    def test_successful_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "program.khan"
            filename.write_text("show 42", encoding="utf-8")

            result = self.run_khan(filename)

            self.assertEqual(result.stdout, "42\n")
            self.assertEqual(result.returncode, 0)

    def test_missing_arguments(self):
        result = subprocess.run(
            [sys.executable, str(PROGRAM)],
            capture_output=True,
            text=True
        )

        self.assertIn("Usage:", result.stdout)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
