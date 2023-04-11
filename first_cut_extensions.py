# define some constants
VARIABLES = {}


# Function to find precedence of operators.
def precedence(op):
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/' or op == '%':
        return 2
    elif op == '^':
        return 3
    elif op == '&' or op == '|' or op == '!':
        return 0
    return -1


def is_number_str(str):
    try:
        x = float(str)
        return True
    except:
        return False


binary_operators = ['+', '-', '*', '/', '^', '%']
boolean_operators = ['&', '|']
unary_operators = ['!']
relational_operators = ['==', '<=', '>=', '!=', '<', '>']


# Function to perform arithmetic operations.
def apply_operation(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return b - a
    elif op == '*':
        return a * b
    elif op == '/':
        return b / a
    elif op == '^':
        return b ** a
    elif op == '%':
        return b % a
    elif op == '&':
        return int(bool(a and b))
    elif op == '|':
        return int(bool(a or b))
    elif op == '==':
        return int(a == b)
    elif op == '<=':
        return int(b <= a)
    elif op == '>=':
        return int(b >= a)
    elif op == '!=':
        return int(a != b)
    elif op == '<':
        return int(b < a)
    elif op == '>':
        return int(b > a)
    else:
        raise Exception('Invalid operator')


def apply_unary_ops(a, op):
    if op == '!':
        return int(bool(not a))
    else:
        raise Exception('Invalid unary operator')


def is_commented(statement):
    statement = statement.strip()
    return statement.startswith('/*') or statement.startswith('#')


def is_op_equals(statement):
    statement = statement.replace(" ", "")
    return any((op + "=") in statement for op in (binary_operators + boolean_operators))


def is_relational_cond(statement):
    statement = statement.replace(" ", "")
    return any(op in statement for op in relational_operators)


def has_assign_var(statement):
    statement = statement.replace(" ", "")
    for i in statement:
        if i.isalpha() or i.isdigit():
            pass
        elif i == '=':
            return True
        else:
            return False
    return False


def relational_cond_var(statement):
    statement = statement.replace(" ", "")
    var = ''
    i = 0
    while i < len(statement):
        if statement[i].isalpha() or statement[i].isdigit():
            var += statement[i]
        elif statement[i] == '=':
            i += 1
            break
        i += 1
    return var, statement[i:]


def op_equals_var(statement):
    statement = statement.replace(" ", "")
    var = ''
    for i in statement:
        if i.isalpha() or i.isdigit():
            var += i
        else:
            return var
    return var


def new_uncommented_line(i, statements):
    statement = statements[i]
    statement = statement.strip()

    if statement.startswith('#'):
        return i + 1
    elif statement.startswith('/*'):
        while i + 1 < (len(statements)) and not statements[i + 1].strip().endswith('*/'):
            i += 1
        return i + 2
    else:
        return i


# Function that returns value of expression after evaluation.
def evaluate(tokens):
    # stack to store integer values.
    values = []
    prev_token_var = False
    # stack to store operators.
    ops = []
    i = 0

    while i < len(tokens):
        # print('------------------>', i, tokens[i])
        # Current token is a whitespace, skip it.
        if tokens[i] == ' ':
            i += 1
            continue

        # Current token is an opening brace, push it to 'ops'
        elif tokens[i] == '(':
            prev_token_var = False
            ops.append(tokens[i])

        # Current token is a number, push it to stack for numbers.
        elif tokens[i].isdigit():
            val_str = ''
            # There may be more than one digit in the number.
            while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                val_str += tokens[i]
                i += 1

            values.append(float(val_str))
            prev_token_var = False
            i -= 1

        # Closing brace encountered, solve entire brace.
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
                values.append(apply_operation(val2, val1, op))

            prev_token_var = False
            # pop opening brace.
            ops.pop()

        elif tokens[i] in (boolean_operators + binary_operators) and i + 1 < len(tokens) and tokens[i + 1] == '=':
            # op-equals extension
            ops.append(tokens[i])
            i += 2
            prev_token_var = False
            continue
        elif tokens[i] in boolean_operators:
            if i + 1 < len(tokens) and tokens[i] == tokens[i + 1]:
                i += 1
            ops.append(tokens[i])
            prev_token_var = False

        elif tokens[i] in relational_operators or (
                i + 1 < len(tokens) and (tokens[i] + tokens[i + 1]) in relational_operators):
            curr_ops = tokens[i]
            if i + 1 < len(tokens) and (tokens[i] + tokens[i + 1]) in relational_operators:
                curr_ops = tokens[i] + tokens[i + 1]
            ops.append(curr_ops)
            prev_token_var = False

        elif tokens[i] in unary_operators:
            curr_ops = tokens[i]
            i += 1
            while i < len(tokens) and tokens[i] == ' ':
                i += 1
            print(i, tokens[i])
            if tokens[i].isdigit():
                val_str = ''
                while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                    val_str += tokens[i]
                    i += 1
                values.append(apply_unary_ops(float(val_str), curr_ops))
                prev_token_var = False
                i -= 1
            else:
                raise Exception('There should be number after ! (negate operation)')

        # Current token is an operator.
        elif tokens[i] in binary_operators:
            # While top of 'ops' has same or greater precedence to current  token, which is an operator
            # ++ / -- cases
            if (tokens[i] == '+' or tokens[i] == '-') and i + 1 < len(tokens) and tokens[i] == tokens[i + 1]:
                # if true, then post ops else pre ops
                if prev_token_var:
                    i += 1
                    # pop last variable and do this operation
                    last_var = values.pop()
                    if last_var in VARIABLES:
                        values.append(VARIABLES[last_var])
                        if tokens[i] == '+':
                            VARIABLES[last_var] += 1
                        else:
                            VARIABLES[last_var] -= 1
                    else:
                        raise Exception('post ++/-- can be applied to variables only')
                else:
                    # get variable which next after ops (as this is pre inc/desc ops)
                    curr_ops = tokens[i]
                    i += 2
                    while i + 1 < len(tokens) and tokens[i + 1] == ' ':
                        i += 1
                    if tokens[i].isalpha():
                        # token is not number
                        variable = ''
                        while i < len(tokens) and (tokens[i].isdigit() or tokens[i].isalpha()):
                            variable += tokens[i]
                            i += 1

                        i -= 1
                        if variable in VARIABLES:
                            if curr_ops == '+':
                                VARIABLES[variable] += 1
                                values.append(VARIABLES[variable])
                            else:
                                VARIABLES[variable] -= 1
                                values.append(VARIABLES[variable])
                        else:
                            raise Exception('post ++/-- can be applied to variables only')

                    else:
                        raise Exception('pre ++/-- can be applied to variables only.')
            # normal single operator case
            else:
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
                    values.append(apply_operation(val2, val1, op))

                # Push current token to 'ops'.
                ops.append(tokens[i])
            prev_token_var = False
        elif tokens[i].isalpha():
            # token is not number
            variable = ''
            while (i < len(tokens) and
                   (tokens[i].isdigit() or tokens[i].isalpha())):
                # val = (val * 10) + int(tokens[i])
                variable += tokens[i]
                i += 1

            values.append(variable)
            prev_token_var = True
            i -= 1
        else:
            prev_token_var = False
            print('************************************ unwanted token', i, ' ----> ', tokens[i])
        i += 1

    # Entire expression has been parsed at this point, apply remaining ops to remaining values.
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
        values.append(apply_operation(val2, val1, op))

    # Top of 'values' contains result, return it.
    if values[-1] in VARIABLES:
        return VARIABLES.get(values[-1])
    return values[-1]


def bc_calculate(input_expression):
    statements = input_expression.split('\n')
    errors = 0
    things_to_be_printed = []
    i = 0
    while i < len(statements):
        statement = statements[i]
        print(statement, ' is being executed........................')
        if statement.strip().startswith('print'):
            # evaluate the expression(s) to be printed
            expr = statement[6:].strip().replace(' ', '')
            exprs = expr.split(',')
            values = []
            for e in exprs:
                value = ''
                try:
                    value = evaluate(e)
                except ZeroDivisionError:
                    value = 'divide by zero'
                    values.append(str(value))
                    break
                except Exception as e:
                    print('parse error', e)
                    # raise e
                    errors += 1
                values.append(str(value))
            things_to_be_printed.append(' '.join(values))
        elif is_commented(statement):
            i = new_uncommented_line(i, statements)
            print('new i= ', i)
            continue
        elif is_op_equals(statement):
            try:
                print('--------------------------------------------------------------')
                print('non assignment -> eval line: ', statement)
                var = op_equals_var(statement)
                VARIABLES[var.strip()] = evaluate(statement.strip())
                print('updated VARIABLES: ', VARIABLES)
                print('--------------------------------------------------------------')
            except ZeroDivisionError:
                things_to_be_printed.append('divide by zero')
                break
            except Exception as e:
                print('parse error', e)
                # raise e
                errors += 1
        elif is_relational_cond(statement):
            if has_assign_var(statement):
                try:
                    print('--------------------------------------------------------------')
                    print('non assignment -> eval line: ', statement)
                    var, exp = relational_cond_var(statement)
                    VARIABLES[var.strip()] = evaluate(exp.strip())
                    print('updated VARIABLES: ', VARIABLES)
                    print('--------------------------------------------------------------')
                except ZeroDivisionError:
                    things_to_be_printed.append('divide by zero')
                    break
                except Exception as e:
                    print('parse error', e)
                    # raise e
            else:
                try:
                    print('--------------------------------------------------------------')
                    print('eval line: ', statement)
                    evaluate(statement)
                    print('updated VARIABLES: ', VARIABLES)
                    print('--------------------------------------------------------------')
                except ZeroDivisionError:
                    things_to_be_printed.append('divide by zero')
                    break
                except Exception as e:
                    print('parse error', e)
                    # raise e
                    errors += 1
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
            except ZeroDivisionError:
                things_to_be_printed.append('divide by zero')
                break
            except Exception as e:
                print('parse error', e)
                # raise e
                errors += 1
        elif statement is None or len(statement) == 0:
            pass
        elif '++' in statement or '--' in statement or any(
                op in statement for op in (binary_operators + boolean_operators + unary_operators)):
            try:
                print('--------------------------------------------------------------')
                print('non assignment -> eval line: ', statement)
                evaluate(statement.strip())
                print('updated VARIABLES: ', VARIABLES)
                print('--------------------------------------------------------------')
            except ZeroDivisionError:
                things_to_be_printed.append('divide by zero')
                break
            except Exception as e:
                print('parse error', e)
                # raise e
                errors += 1
        else:
            print('Unidentified input statement', statement)

        i += 1
    print('----------------------------<MAIN EXECUTION PRINT>------------------------')
    if errors == 0:
        for p in things_to_be_printed:
            print(p)
    else:
        print('parse error')


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
# bc_calculate(input_str2)

input_str3 = """x = 2
x1 = 3
x2 = 6.5
y1 = x1 + x2
y2 = x1 + x2 * 2
y3 = x2 / x1 - x
y4 = x2 % 2
y5 = x1 ^ 2
print x,x1,x2, y1, y2, y3,y4
"""
# bc_calculate(input_str3)

input_str4 = """x = 0
y = 5
x+ y
z = x++ + y
++y
print x++ + y, x, y, z"""
# bc_calculate(input_str4)

input_str5 = """
print 5 - 1 - 1 - 1
print ((5 - 1) - 1) - 1
print 2 ^ 2 ^ 2

"""
# bc_calculate(input_str5)

input_str6 = """
print 0/1, 1/0
1/ 
"""
# bc_calculate(input_str6)

input_str7 = """
x = 1
y = 2
print x, y
/* z = 3
w = 4
i = 3 */
x = 3
# i have changed x
print x, y
"""
# bc_calculate(input_str7)

input_str8 = """
1 && 2
2 && 1
1 || 0
0 && 1
!10
print 1 && 2, 2 && 1, 1 || 0, 0 && 1, !1, !0, !10, !15
"""
# bc_calculate(input_str8)

input_str9 = """
x= 1
x+=3
x-=2
x*=3
x/=1.5
x^=4
print x
"""
# bc_calculate(input_str9)

input_str10 = """
x = 1 > 5
y = 6 > 3
print x,y, 6 >= 6, 7<=8, 4==4, 5!=4, 9!=9
"""
bc_calculate(input_str10)