import re

# Define regex patterns
NUM_PATTERN = r'(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
VAR_PATTERN = r'[a-zA-Z_]\w*'
OP_PATTERN = r'[+\-*/%^()]'
ASSIGN_PATTERN = r'\s*({var})\s*=\s*({num}|{var}(?:\s*{op}\s*{num}|))(?:$|#|//)'.format(var=VAR_PATTERN,
                                                                                        num=NUM_PATTERN, op=OP_PATTERN)
# PRINT_PATTERN = r'\s*print\s+({var}(?:\s*{op}\s*{var})*)(?:\s*,\s*({var}(?:\s*{op}\s*{var})*)+)*(?:$|#|//)'.format(
#     var=VAR_PATTERN, op=OP_PATTERN)
PRINT_PATTERN = r'\s*print\s+({var}(?:\s*{op}\s*{var})*)(?:\s*,\s*({var}(?:\s*{op}\s*{var})*))*\s*'.format(
    var=VAR_PATTERN, op=OP_PATTERN)

EXPR_PATTERN = r'^\s*({num}|{var}|\({expr}\))(?:\s*{op}\s*({num}|{var}|\({expr}\)))*\s*$'.format(num=NUM_PATTERN,
                                                                                                 var=VAR_PATTERN,
                                                                                                 op=OP_PATTERN,
                                                                                                 expr='(?:{num}|{var}|\({expr}\))(?:\s*{op}\s*(?:{num}|{var}|\({expr}\)))*'.format(
                                                                                                     num=NUM_PATTERN,
                                                                                                     var=VAR_PATTERN,
                                                                                                     op=OP_PATTERN,
                                                                                                     expr='{expr}'))

# Define precedence of operators
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '**': 3, '(': 0, ')': 0}

# Define error messages
PARSE_ERROR_MSG = 'parse error'
DIVISION_BY_ZERO_MSG = 'divide by zero'

# Define global variable dictionary
VARIABLES = {}


def parse(program):
    statements = program.strip().split('\n')
    for statement in statements:
        match = re.match(ASSIGN_PATTERN, statement)
        if match:
            var_name = match.group(1)
            expr = match.group(2)
            try:
                value = evaluate(expr)
                VARIABLES[var_name] = value
            except ZeroDivisionError:
                print(DIVISION_BY_ZERO_MSG)
                return
            except Exception as e:
                print(e)
                print(PARSE_ERROR_MSG)
                return
        elif '=' in statement:
            args = statement.split("=")
            if len(args) != 2:
                print(PARSE_ERROR_MSG)
                continue
            var_name = args[0].strip()
            expr = args[1].strip()

            try:
                value = evaluate(expr)
                VARIABLES[var_name] = value
            except ZeroDivisionError:
                print(DIVISION_BY_ZERO_MSG)
                return
            except Exception as e:
                print(e)
                print(PARSE_ERROR_MSG)
                return
        elif statement.strip().startswith('print'):
            statement = statement[5:]
            exprs = statement.split(',')
            try:
                values = []
                for e in exprs:
                    if e is not None:
                        e = e.strip()
                        value = evaluate(e)
                        values.append(str(value))
                print(' '.join(values))
            except ZeroDivisionError:
                print(DIVISION_BY_ZERO_MSG)
                return
            except Exception as e:
                print(e)
                print(PARSE_ERROR_MSG)
                return
        else:
            print('invalid input:', PARSE_ERROR_MSG )
            # print(PARSE_ERROR_MSG)
            return


def evaluate_postfix(postfix_tokens):
    operand_stack = []
    for token in postfix_tokens:
        if token.isdigit():
            operand_stack.append(float(token))
        elif is_variable(token):
            operand_stack.append(VARIABLES[token])
        else:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            elif token == '^':
                result = operand1 ** operand2
            else:
                result = None
            operand_stack.append(result)
    return operand_stack.pop()


def precedence(op):
    return PRECEDENCE.get(op, -1)


def is_number(token):
    return re.match(NUM_PATTERN, token) is not None


def is_variable(token):
    return re.match(VAR_PATTERN, token) is not None


def tokenize(expr):
    tokens = []
    for match in re.finditer(EXPR_PATTERN, expr):
        tokens.append(match.group(0))
    return tokens



def evaluate(expr):
    tokens = tokenize(expr)
    postfix_tokens = infix_to_postfix(tokens)
    return evaluate_postfix(postfix_tokens)


def infix_to_postfix(tokens):
    postfix_tokens = []
    operator_stack = []
    for token in tokens:
        if is_number(token) or is_variable(token):
            postfix_tokens.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                postfix_tokens.append(operator_stack.pop())
            operator_stack.pop()
        else:
            while operator_stack and operator_stack[-1] != '(' and precedence(operator_stack[-1]) >= precedence(token):
                postfix_tokens.append(operator_stack.pop())

    return postfix_tokens


input_str = '''x  = 3
y  = 5
z  = 2 + x * y
z2 = (2 + x) * y
print x, y, z, z2'''
parse(input_str)
