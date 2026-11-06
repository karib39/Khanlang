from khan_ast import BinaryOp, UnaryOp, Variable, String, evaluate_ast, FunctionCall


def parse_number(tokens):
    if len(tokens) != 1:
        raise ValueError("EXpected exactly one number")
    token = tokens[0]

    if isinstance(token, (int, float)) and not isinstance(token, bool):
        return token

    raise ValueError(f"Expected a number, got {token!r}")

def split_arguments(tokens):
    if not tokens:
        return []

    arguments = []
    current_arguments = []
    depth = 0

    for token in tokens:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1

        if token == "," and depth == 0:
            if not current_arguments:
                raise SyntaxError("Missing function argument")
            arguments.append(current_arguments)
            current_arguments = []
        else:
            current_arguments.append(token)

    if not current_arguments:
        raise SyntaxError("Missing function arguments")
    arguments.append(current_arguments)

    return arguments

def parse_factor(tokens):
    if len(tokens) == 1:
        if isinstance(tokens[0], String):
            return tokens[0]
        if isinstance(tokens[0], Variable):
            return tokens[0]
        return parse_number(tokens)

    if len(tokens) >= 3 and isinstance(tokens[0], Variable):
        if tokens[1] == "(" and tokens[-1] == ")":
            name = tokens[0].name

            argument_tokens = split_arguments(tokens[2:-1])

            arguments = [
                parse_expression(argument)
                for argument in argument_tokens
            ]

            return FunctionCall(name, arguments)

    if tokens and tokens[0] == "-":
        operand = parse_factor(tokens[1:])
        return UnaryOp("-", operand)


    if is_wrapped_in_parentheses(tokens):
        inner_tokens = tokens[1:-1]
        return parse_expression(inner_tokens)

    raise ValueError("Invalid FActor")

def is_wrapped_in_parentheses(tokens):
    if len(tokens) < 2:
        return False

    if tokens[0] != "(" or tokens[-1] != ")":
        return False

    depth = 0

    for index, token in enumerate(tokens):
        if token == "(":
            depth += 1

        elif token == ")":
            depth -= 1

        elif depth == 0 and index < len(tokens):
            return False

    return depth == 0


def find_factor_end(tokens, start):
    if start >= len(tokens):
        raise ValueError("Expected a factor")

    if tokens[start] == "-":
        return find_factor_end(tokens, start + 1)

    if isinstance(tokens[start], Variable) and start + 1 < len(tokens):
        if tokens[start + 1] == "(":
            depth = 0

            for i in range(start + 1, len(tokens)):
                if tokens[i] == "(":
                    depth += 1
                elif tokens[i] == ")":
                    depth -= 1

                    if depth == 0:
                        return i

            raise ValueError("Unclosed function call")

    if tokens[start] != "(":
        return start



def parse_term(tokens):
    if not tokens:
        raise ValueError("Expected a term")

    start = 0
    end = find_factor_end(tokens, start)
    left = parse_factor(tokens[start:end + 1])

    i = end + 1

    while i < len(tokens):
        operator = tokens[i]

        if operator not in ["*", "/"]:
            raise ValueError(f"Unexpected operator: {operator!r}")

        start = i + 1
        if start >= len(tokens):
            raise  ValueError("Missing  right operand")
        if tokens[start] in ["*","/","+"]:
            raise ValueError("Expected a factor after operator")
        end = find_factor_end(tokens, start)
        right = parse_factor(tokens[start:end + 1])

        left = BinaryOp(operator, left, right)

        i = end + 1

    return left


def validate_parentheses(tokens):
    depth = 0

    for token in tokens:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1

            if depth < 0:
                raise ValueError("Unexpected closing parentheses")

    if depth > 0:
        raise ValueError("Unlosed parentheses")

def find_comparison_index(tokens):
    depth = 0
    comparison_index = -1

    for index, token in enumerate(tokens):
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1

        elif token in ["==","!=",">","<","<=",">="] and depth == 0:
            if comparison_index != -1:
                raise SyntaxError("Multiple comparison operators are not supported")
            comparison_index = index
    return comparison_index



def parse_expression(tokens):

    if not tokens:
        raise ValueError("Expected an expression")

    validate_parentheses(tokens)

    comparison_index = find_comparison_index(tokens)

    if comparison_index != -1:
        left_token = tokens[:comparison_index]
        operator = tokens[comparison_index]
        right_token = tokens[comparison_index + 1:]

        left = parse_expression(left_token)
        right = parse_expression(right_token)

        return BinaryOp(operator, left, right)


    if is_wrapped_in_parentheses(tokens):
        return parse_expression(tokens[1:-1])
    split_index = find_split_index(tokens)

    if split_index != -1:
        if split_index == 0 and split_index == len(tokens) - 1:
            raise ValueError("missing operand")

        left_token = tokens[:split_index]
        operator = tokens[split_index]
        right_token = tokens[split_index + 1:]

        left = parse_expression(left_token)
        right = parse_term(right_token)
        return BinaryOp(operator, left, right)
    return parse_term(tokens)


def find_split_index(tokens):
    depth = 0
    split_index = -1

    for index,token in enumerate(tokens):
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
        elif token in ["+", "-"] and depth == 0:
            if index == 0 or tokens[index - 1] in ["+", "-", "*", "/", "("]:
                continue
            split_index = index
    return split_index
