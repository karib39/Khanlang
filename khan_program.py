
from khan_lexer import tokenize
from khan_ast import evaluate_ast
from statement import (
    parse_assignment,
    parse_show,
    parse_if,
    parse_while,
    parse_func,
    convert_expression_tokens
)
from expr_parser import parse_expression

import sys
from pathlib import Path


def split_statements(source_code):
    lines = source_code.splitlines()

    statements = []
    current_statement = []
    brace_depth = 0

    for line in lines:
        if not line.strip():
            continue

        current_statement.append(line)

        tokens = tokenize(line)

        for token in tokens:
            if token.type == "BRACE":
                if token.value == "{":
                    brace_depth += 1

                elif token.value == "}":
                    brace_depth -= 1

                    if brace_depth < 0:
                        raise SyntaxError("Unexpected closing '}'")

        if brace_depth == 0:
            statements.append("\n".join(current_statement))
            current_statement = []

    if brace_depth != 0:
        raise SyntaxError("Missing closing '}'")

    if current_statement:
        raise SyntaxError("Incomplete statement")

    return statements


def run_program(source_code):
    statements = split_statements(source_code)

    environment = {}
    functions = {}

    # First pass: register function definitions.
    for statement in statements:
        tokens = tokenize(statement)

        if not tokens:
            continue

        if tokens[0].value == "func":
            function = parse_func(tokens)

            if function.name in functions:
                raise SyntaxError(
                    f"Function '{function.name}' is already defined"
                )

            functions[function.name] = function

    # Second pass: execute the program.
    for statement in statements:
        tokens = tokenize(statement)

        if not tokens:
            continue

        if tokens[0].value == "func":
            continue

        elif tokens[0].value == "create":
            ast = parse_assignment(tokens)

        elif tokens[0].value == "show":
            ast = parse_show(tokens)

        elif tokens[0].value == "if":
            ast = parse_if(tokens)

        elif tokens[0].value == "while":
            ast = parse_while(tokens)

        elif (
            tokens[0].type == "WORD"
            and len(tokens) > 1
            and tokens[1].value == "("
        ):
            converted = convert_expression_tokens(tokens)
            ast = parse_expression(converted)

        else:
            raise SyntaxError(
                f"Unexpected statement: {tokens[0].value}"
            )

        evaluate_ast(ast, environment, functions)

    return environment


def main():
    if len(sys.argv) != 2:
        print("Usage: khan <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Validate the file extension before opening the file.
    if Path(filename).suffix.lower() != ".khan":
        print("Error: Khanlang files must use the .khan extension.")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source_code = file.read()

        run_program(source_code)

    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)

    except PermissionError:
        print(f"Error: Permission denied while reading {filename}")
        sys.exit(1)

    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as error:
        print(f"Khanlang Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
