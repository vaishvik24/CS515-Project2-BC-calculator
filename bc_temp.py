import re


class ParseError(Exception):
    pass


class DivideByZeroError(Exception):
    pass


def parse_program(program):
    statements = []
    for ip_line in program.strip().split("\n"):
        line = re.sub(r'\s+', '', ip_line)  # remove all whitespace
        print('line: ', line)
        if not line or line == '' or line is None or len(line) < 2:
            continue
        if line.startswith("print"):
            expressions = re.findall(r"\((.*?)\)", line)  # find all parenthesized expressions
            if not expressions:
                raise ParseError("print statement with no expressions")
            expressions = [parse_expression(e) for e in expressions]
            statements.append(("print", expressions))
        elif "=" in line:
            variable, expression = line.split("=")
            variable = parse_variable(variable)
            expression = parse_expression(expression)
            statements.append(("assign", variable, expression))
        else:
            expression = parse_expression(line)
            statements.append(("expr", expression))
    return statements


def parse_expression(expression):
    # Check for increment/decrement operators
    if "++" in expression or "--" in expression:
        if expression.count("++") + expression.count("--") != 1:
            raise ParseError("too many increment/decrement operators")
        if not re.match(r"^[a-zA-Z]\w*$", expression.replace("++", "").replace("--", "")):
            raise ParseError("increment/decrement operators only apply to variables")
        op = "++" if "++" in expression else "--"
        var = parse_variable(expression.replace(op, ""))
        return (op[:-1], var)
    # Check for unary negation
    if expression.startswith("-"):
        return ("negate", parse_expression(expression[1:]))
    # Check for binary operators
    for op in ["+", "-", "*", "/", "%", "^"]:
        if op in expression:
            left, right = [parse_expression(e) for e in expression.split(op, 1)]
            return (op, left, right)
    # Check for parentheses
    if expression.startswith("(") and expression.endswith(")"):
        return parse_expression(expression[1:-1])
    # Check for constants and variables
    if re.match(r"^\d+(\.\d+)?$", expression):
        return float(expression)
    if re.match(r"^[a-zA-Z]\w*$", expression):
        return parse_variable(expression)
    raise ParseError("invalid expression")


def parse_variable(variable):
    if not re.match(r"^[a-zA-Z]\w*$", variable):
        raise ParseError("invalid variable name")
    return variable


def evaluate_program(statements):
    variables = {}
    output = []
    for statement in statements:
        if statement[0] == "print":
            output.extend([evaluate_expression(e, variables) for e in statement[1]])
        elif statement[0] == "assign":
            var = statement[1]
            expr = statement[2]
            val = evaluate_expression(expr, variables)
            variables[var] = val
        elif statement[0] == "expr":
            val = evaluate_expression(statement[1], variables)
        else:
            raise ValueError("invalid statement type: {}".format(statement[0]))
    return output


def evaluate_expression(expression, variables):
    if isinstance(expression, float):
        return expression
    elif isinstance(expression, str):
        if expression not in variables:
            variables[expression] = 0.0
        return variables[expression]
    elif expression[0] == "negate":
        return -evaluate_expression(expression[1], variables)
    elif expression[0] == "++":
        var = expression[1]
        if var not in variables:
            raise ValueError("undefined variable: {}".format(var))
        value = variables[var] + 1
        variables[var] = value
        return value
    elif expression[0] == "--":
        var = expression[1]
        if var not in variables:
            raise ValueError("undefined variable: {}".format(var))
        value = variables[var] - 1
        variables[var] = value
        return value
    elif expression[0] in ["+", "-", "*", "/", "%", "^"]:
        left = evaluate_expression(expression[1], variables)
        right = evaluate_expression(expression[2], variables)
        if expression[0] == "+":
            return left + right
        elif expression[0] == "-":
            return left - right
        elif expression[0] == "*":
            return left * right
        elif expression[0] == "/":
            if right == 0:
                raise DivideByZeroError("division by zero")
            return left / right
        elif expression[0] == "%":
            if right == 0:
                raise DivideByZeroError("modulo by zero")
            return left % right
        elif expression[0] == "^":
            return left ** right
    else:
        raise ValueError("invalid expression type: {}".format(expression[0]))


# statements = """"
#                 x  = 3
#                 y  = 5
#                 z  = 2 + x * y
#                 z2 = (2 + x) * y
#                 print x, y, z, z2
#             """
statements = """"
                x  = 3
                y  = 5
                print x, y
            """

parse_program(statements)
