class BinaryOp:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class UnaryOp:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
class Variable:
    def __init__(self, name):
        self.name = name

class String:
    def __init__(self, value):
        self.value = value

class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
class Show:
    def __init__(self, expression):
        self.expression = expression

class Conditional:
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
class Return:
    def __init__(self, expression):
        self.expression = expression
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

def evaluate_ast(node, environment=None, functions=None):
    if environment is None:
        environment = {}

    if functions is None:
        functions = {}

    if isinstance(node, bool):
        return node

    if isinstance(node, (int, float)):
        return node

    elif isinstance(node, Variable):
        if node.name not in environment:
            raise NameError(f"Undefined variable: {node.name}")
        return environment[node.name]

    elif isinstance(node, String):
        return node.value

    elif isinstance(node, Assignment):
        value = evaluate_ast(node.value, environment, functions)
        environment[node.name] = value
        return value
    elif isinstance(node, Show):
        value = evaluate_ast(node.expression, environment, functions)
        print(value)
        return value
    elif isinstance(node, BinaryOp):
        left = evaluate_ast(node.left, environment, functions)
        right = evaluate_ast(node.right, environment, functions)

        left_is_number = type(left) in (int, float)
        right_is_number = type(right) in (int, float)

        left_is_string = isinstance(left, str)
        right_is_string = isinstance(right, str)

        if node.operator in ("==","!=",">","<","<=",">="):
            if node.operator in ("==","!="):
                if left_is_number and right_is_number:
                    pass
                elif left_is_string and right_is_string:
                    pass
                else:
                    raise TypeError("Equality comparisons requires matching types")

            elif not (left_is_number and right_is_number):
                    raise TypeError("Ordering comparisons requires number")

            if node.operator == "==":
                return left == right

            elif node.operator == "!=":
                return left != right

            elif node.operator == ">":
                return left > right

            elif node.operator == "<":
                return left < right

            elif node.operator == ">=":
                return left >= right

            elif node.operator == "<=":
                return left <= right

        if node.operator == "+":
            if left_is_number and right_is_number:
                return left + right
            elif left_is_string and right_is_string:
                return left + right
            else:
                raise TypeError("Cannot add a string and a number")

        elif node.operator in ("-","*","/"):
            if not (left_is_number and right_is_number):
                raise TypeError(f"Operator '{node.operator}' requires number")
            if node.operator == "*":
                return left * right
            elif node.operator == "-":
                return left - right
            elif node.operator == "/":
                if right == 0:
                    raise ZeroDivisionError(f"{left} cant be divided by zero")
                return left / right

    elif isinstance(node, UnaryOp):
        operand = evaluate_ast(node.operand, environment, functions)
        if node.operator == "-":
            return -operand

        raise ValueError(f"Unknown unary operator: {node.operator}")

    elif isinstance(node, Conditional):
        condition = evaluate_ast(node.condition, environment, functions)


        if not isinstance(condition, bool):
            raise TypeError("Condition must evaluate to True or False")

        if condition:
            body = node.if_body
        else:
            body = node.else_body

        result = None

        if body is not None:
            for statement in body:
                result = evaluate_ast(statement, environment, functions)

        return result

    elif isinstance(node, WhileLoop):
        result = None

        itr = 0
        max_itr = 10000
        while True:
            condition = evaluate_ast(node.condition, environment, functions)
            if not isinstance(condition, bool):
                raise TypeError("Loop must evaluate to True or False")
            if not condition:
                break
            if itr >= max_itr:
                raise RuntimeError("Maximum loop iteration reached")
            itr += 1
            for statement in node.body:
                result = evaluate_ast(statement, environment, functions)
        return result

    elif isinstance(node, FunctionCall):
        if node.name not in functions:
            raise NameError(f"Undefined function: {node.name}")

        function = functions[node.name]

        if len(node.arguments) != len(function.parameters):
            raise TypeError(
                f"Function '{node.name}' expects "
                f"{len(function.parameters)} arguments, "
                f"got {len(node.arguments)}"
            )

        argument_values = [
            evaluate_ast(argument, environment, functions)
            for argument in node.arguments
        ]

        local_environment = environment.copy()

        for parameter, value in zip(function.parameters, argument_values):
            local_environment[parameter] = value

        try:
            for statement in function.body:
                evaluate_ast(statement, local_environment, functions)
        except ReturnSignal as signal:
            return signal.value

        return None

    elif isinstance(node, Return):
        value = evaluate_ast(node.expression, environment,functions)
        raise ReturnSignal(value)
