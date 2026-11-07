# Khanlang

Khanlang is a small, beginner-friendly programming language implemented in Python.

It is an educational project created to explore how programming languages and interpreters work.

## Features

- Variables and assignment
- Numbers and strings
- Arithmetic and expressions
- Operator precedence and parentheses
- Type checking
- Conditional statements (`if` / `else`)
- `while` loops
- Functions with parameters and return values
- Nested conditions and loops
- Function calls and local scope
- Error handling
- Command-line execution

## Requirements

- Python 3.8 or newer (declared minimum; compatibility testing is pending)

## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/karib39/Khanlang.git
cd Khanlang
```

Install Khanlang:

```bash
python -m pip install .
```

Run a Khanlang program:

```bash
khan hello.khan
```

Alternatively, run a program directly without installing:

```bash
python khan_program.py hello.khan
```

## Example

Create a file named `hello.khan`:

```khanlang
func add(a, b) {
    return a + b
}

create result = add(10, 20)
show result
```

Output:

```text
30
```

## Running Tests

Install pytest:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest -v
```

## Project Status

Khanlang is a personal learning project. It is being developed to explore interpreter design and programming language implementation.

It is not intended to replace established programming languages or serve as a production-ready language.

## License

Khanlang is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
