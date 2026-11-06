from expr_parser import parse_expression
from khan_ast import Assignment, Variable, String, Show, Conditional, WhileLoop, FunctionDef, Return


def convert_expression_tokens(tokens):
    converted = []

    for token in tokens:
        if token.type == "NUMBER":
            converted.append(token.value)
        elif token.type == "OPERATOR":
            converted.append(token.value)
        elif token.type == "COMPARISON":
            converted.append(token.value)
        elif token.type == "WORD":
            converted.append(Variable(token.value))
        elif token.type == "STRING":
            converted.append(String(token.value))
        elif token.type == "PUNCTUATION":
            converted.append(token.value)
        else:
            raise SyntaxError(f"Unexpected token: {token.value}")
    return converted


def parse_assignment(tokens):
    if len(tokens) < 4:
        raise SyntaxError("Incomplete assignment")
    if tokens[0].type != "KEYWORD" or tokens[0].value != "create":
        raise SyntaxError("Expected 'create'")
    if tokens[1].type != "WORD":
        raise SyntaxError("Expected a variable name")
    if tokens[2].type != "EQUALS":
        raise SyntaxError("Expected '='")


    name = tokens[1].value
    expression_tokens = tokens[3:]
    converted = convert_expression_tokens(expression_tokens)
    expression = parse_expression(converted)
    return Assignment(name, expression)

def parse_show(tokens):
    if len(tokens) < 2:
        raise SyntaxError("Expected an expression after 'show'")

    if tokens[0].type != "KEYWORD" or tokens[0].value != "show":
        raise SyntaxError("Expected 'show'")

    expression_tokens = tokens[1:]
    converted = convert_expression_tokens(expression_tokens)
    expression = parse_expression(converted)

    return Show(expression)

def parse_return(tokens):
    if not tokens or tokens[0].value != "return":
        raise SyntaxError("Expected 'return'")

    if len(tokens) < 2:
        raise SyntaxError("Expected an Expression  affter 'return'")

    expression_tokens = tokens[1:]
    converted = convert_expression_tokens(expression_tokens)
    expression = parse_expression(converted)

    return Return(expression)

def parse_func(tokens):
    if len(tokens) < 4:
        raise SyntaxError("Incomplete function definition")

    if tokens[0].type != "KEYWORD" or tokens[0].value != "func":
        raise SyntaxError("Expected 'func'")

    if tokens[1].type != "WORD":
        raise SyntaxError("Expected a function name")

    if tokens[2].type != "PUNCTUATION" or tokens[2].value != "(":
        raise SyntaxError("Expected '('")

    name = tokens[1].value
    parameters = []
    index = 3

    while index < len(tokens):
        if tokens[index].value == ")":
            break

        if tokens[index].type != "WORD":
            raise SyntaxError("Expected parameter name")

        if tokens[index].value in parameters:
            raise SyntaxError("Duplicate parameter name")

        parameters.append(tokens[index].value)
        index += 1

        if index >= len(tokens):
            raise SyntaxError("Expected ')'")

        if tokens[index].value == ")":
            break

        if tokens[index].value != ",":
            if tokens[index].value == "{":
                raise SyntaxError("Expected ')' before function body")
            raise SyntaxError("Expected ',' between parameters")

        index += 1

        if index >= len(tokens) or tokens[index].value == ")":
            raise SyntaxError("Expected parameter after ','")

    if index >= len(tokens) or tokens[index].value != ")":
        raise SyntaxError("Expected ')'")

    index += 1

    if index >= len(tokens):
        raise SyntaxError("Expected '{' after parameters")

    if tokens[index].type != "BRACE" or tokens[index].value != "{":
        raise SyntaxError("Expected '{' after parameters")

    body_start = index

    body, next_index = parse_block(tokens, body_start)

    if next_index != len(tokens):
        raise SyntaxError("Unexpected tokens after function definition")

    return FunctionDef(name, parameters, body)

def parse_block(tokens, start_index):
    if tokens[start_index].type != "BRACE" or tokens[start_index].value != "{":
        raise SyntaxError("Expected '{'")

    body = []
    index = start_index + 1

    while index < len(tokens):
        if tokens[index].type == "BRACE" and tokens[index].value == "}":
            return body, index + 1

        statement_start = index

        nested_depth = 0

        while index < len(tokens):
            token = tokens[index]

            if token.type == "BRACE":
                if token.value == "{":
                    nested_depth += 1

                elif token.value == "}":
                    if nested_depth == 0:
                        break
                    nested_depth -= 1

            if nested_depth == 0 and index > statement_start:
                if token.type == "KEYWORD":
                    if token.value in ("create","show","if","while","return","func"):
                        break

            index += 1

        statement_tokens = tokens[statement_start:index]

        if not statement_tokens:
            raise SyntaxError("Empty or invalid statement in block")

        if statement_tokens[0].value == "create":
            statement = parse_assignment(statement_tokens)

        elif statement_tokens[0].value == "show":
            statement  = parse_show(statement_tokens)

        elif statement_tokens[0].value == "if":
            statement = parse_if(statement_tokens)

        elif statement_tokens[0].value == "while":
            statement = parse_while(statement_tokens)

        elif statement_tokens[0].value == "return":
            statement = parse_return(statement_tokens)

        elif statement_tokens[0].value == "func":
            statement = parse_func(statement_tokens)

        else:
            raise SyntaxError(
                f"Unexpected statement in block: {statement_tokens[0].value}"
            )

        body.append(statement)

    raise SyntaxError("Missing closing '}'")



def parse_if(tokens):
    if not tokens or tokens[0].type != "KEYWORD" or tokens[0].value != "if":
        raise SyntaxError("Expected 'if'")

    body_start = next(
            (i for i , token in enumerate(tokens) if token.type == "BRACE" and token.value == "{"), -1

            )

    if body_start == -1:
        raise SyntaxError("Expected '{' after condition")

    condition_tokens = tokens[1:body_start]

    if not condition_tokens:
        raise SyntaxError("Expected condition after 'if'")

    converted = convert_expression_tokens(condition_tokens)
    condition = parse_expression(converted)

    if_body, next_index = parse_block(tokens, body_start)

    else_body = None

    if next_index < len(tokens):
        if tokens[next_index].type != "KEYWORD" or tokens[next_index].value != "else":
            raise SyntaxError("Unexpected token after 'if' block")

        else_start = next_index + 1
        else_body, next_index = parse_block(tokens, else_start)

    if next_index != len(tokens):
        raise SyntaxError("Unexpected tokens after conditional")

    return Conditional(condition, if_body, else_body)

def parse_while(tokens):
    if not tokens or tokens[0].type != "KEYWORD" or tokens[0].value != "while":
        raise SyntaxError("Expected 'while'")

    body_start = next(
        (i for i, token in enumerate(tokens)
         if token.type == "BRACE" and token.value == "{"),
        -1
    )

    if body_start == -1:
        raise SyntaxError("Expected '{' after loop condition")

    condition_tokens = tokens[1:body_start]

    if not condition_tokens:
        raise SyntaxError("Expected condition after 'while'")

    converted = convert_expression_tokens(condition_tokens)
    condition = parse_expression(converted)

    body, next_index = parse_block(tokens, body_start)

    if next_index != len(tokens):
        raise SyntaxError("Unexpected tokens after while loop")

    return WhileLoop(condition, body)
