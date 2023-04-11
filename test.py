import math

# define some constants
VARIABLES = {}


# Python3 program to evaluate a given
# expression where tokens are
# separated by space.

# Function to find precedence
# of operators.
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%':
        return 2
    if op == '^':
        return 3
    return 0


def is_number_str(str):
    try:
        x = float(str)
        return True
    except:
        return False


# Function to perform arithmetic
# operations.
def applyOp(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b
    if op == '^': return a ** b


# Function that returns value of expression after evaluation.
def evaluate(tokens):
    # stack to store integer values.
    values = []

    # stack to store operators.
    ops = []
    i = 0

    while i < len(tokens):

        # Current token is a whitespace, skip it.
        if tokens[i] == ' ':
            i += 1
            continue

        # Current token is an opening brace, push it to 'ops'
        elif tokens[i] == '(':
            ops.append(tokens[i])

        # Current token is a number, push it to stack for numbers.
        elif tokens[i].isdigit():
            # val = 0
            val_str = ''
            # There may be more than one digit in the number.
            while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                # val = (val * 10) + int(tokens[i])
                val_str += tokens[i]
                i += 1

            values.append(float(val_str))

            i -= 1

        # Closing brace encountered,
        # solve entire brace.
        elif tokens[i] == ')':

            while len(ops) != 0 and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                print('helper::  ---> ', val2, op, val1)
                if not is_number_str(val1):
                    if val1 in VARIABLES:
                        val1 = VARIABLES.get(val1)
                    else:
                        print(val1, ' is not in variable list. (1)')

                if not is_number_str(val2):
                    if val2 in VARIABLES:
                        val2 = VARIABLES.get(val2)
                    else:
                        print(val2, ' is not in variable list. (1)')
                print('--------------------> helper::  ---> ', val2, op, val1)
                values.append(applyOp(val1, val2, op))

            # pop opening brace.
            ops.pop()

        # Current token is an operator.
        elif tokens[i] in '+-*/^':
            # While top of 'ops' has same or greater precedence to current  token, which is an operator.
            # Apply operator on top of 'ops' to top two elements in values stack.
            while len(ops) != 0 and precedence(ops[-1]) >= precedence(tokens[i]):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                print('helper::  ---> ', val2, op, val1)
                if not is_number_str(val1):
                    if val1 in VARIABLES:
                        val1 = VARIABLES.get(val1)
                    else:
                        print(val1, ' is not in variable list. (1)')

                if not is_number_str(val2):
                    if val2 in VARIABLES:
                        val2 = VARIABLES.get(val2)
                    else:
                        print(val2, ' is not in variable list. (1)')
                print('--------------------> helper::  ---> ', val2, op, val1)
                values.append(applyOp(val1, val2, op))

            # Push current token to 'ops'.
            ops.append(tokens[i])
        else:
            # token is not number
            variable = ''
            while (i < len(tokens) and
                   (tokens[i].isdigit() or tokens[i].isalpha())):
                # val = (val * 10) + int(tokens[i])
                variable += tokens[i]
                i += 1

            values.append(variable)
            i -= 1

        i += 1

    # Entire expression has been parsed
    # at this point, apply remaining ops
    # to remaining values.
    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        print('helper::  ---> ', val2, op, val1)
        if not is_number_str(val1):
            if val1 in VARIABLES:
                val1 = VARIABLES.get(val1)
            else:
                print(val1, ' is not in variable list. (1)')

        if not is_number_str(val2):
            if val2 in VARIABLES:
                val2 = VARIABLES.get(val2)
            else:
                print(val2, ' is not in variable list. (1)')
        print('--------------------> helper::  ---> ', val2, op, val1)
        values.append(applyOp(val1, val2, op))

    # Top of 'values' contains result,
    # return it.
    if values[-1] in VARIABLES:
        return VARIABLES.get(values[-1])
    return values[-1]


def bc_calculate(input_str):
    statements = input_str.split('\n')
    for statement in statements:
        if statement.startswith('print'):
            # evaluate the expression(s) to be printed
            expr = statement[6:].strip().replace(' ', '')
            exprs = expr.split(',')
            try:
                values = []
                for e in exprs:
                    value = evaluate(e)
                    values.append(str(value))
                print(' '.join(values))
            except ZeroDivisionError:
                print('Division by zero')
            except Exception as e:
                raise e
        elif '=' in statement:
            # assign a value to a variable
            var, expr = statement.split('=')
            try:
                print('--------------------------------------------------------------')
                print('eval line: ', statement)
                value = evaluate(expr.strip())
                print('value: ', value)
                VARIABLES[var.strip()] = value
                print('updated VARIABLES: ', VARIABLES)
                print('--------------------------------------------------------------')
            except Exception as e:
                raise e
        else:
            print('not print or assignment type statement')


# split input into individual statements and evaluate each one
input_str = """x = 3
y = 5
z = 2 + x * y
z2 = (2 + x) * y
print x, y, z, z2"""
# bc_calculate(input_str)

input_str2 = """pi = 3.14159
r = 2
area = pi * r^2
print area"""
bc_calculate(input_str2)
