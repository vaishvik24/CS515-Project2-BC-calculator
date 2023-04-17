import sys

# stores all the variables defined in the inputs
VARIABLES = {}


# Function to find precedence of operators.
def precedence(op):
    """
    Return the precedence order of the operator
    :param op: operator
    :return: precedence order
    """
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/' or op == '%':
        return 2
    elif op == '^':
        return 3
    elif op == '&' or op == '|' or op == '!':
        return 0
    return -1


def is_number_(s):
    """
    Checks whether string is a number or not
    :param s: string
    :return: boolean
    """
    try:
        float(s)
        return True
    except:
        return False


def is_var_name(s):
    """
    Checks if string is variable or number
    :param s:
    :return:
    """
    i = 0
    if s[i].isalpha():
        while i < len(s) and (s[i].isalnum() or s[i] == '_'):
            i += 1
        return i == len(s)
    else:
        return False


# some predefined operator symbols
binary_operators = ['+', '-', '*', '/', '^', '%']
boolean_operators = ['&', '|']
unary_operators = ['!']
relational_operators = ['==', '<=', '>=', '!=', '<', '>']


# Function to perform arithmetic operations.
def apply_operation(a, b, op):
    """
    Takes float/int args and apply binary operation on it and return calculated result
    :param a: float number input 1
    :param b: float number input 2
    :param op: operation
    :return: evaluated number
    """
    if op == '+':
        return float(a + b)
    elif op == '-':
        return float(b - a)
    elif op == '*':
        return float(a * b)
    elif op == '/':
        return float(b / a)
    elif op == '^':
        return float(b ** a)
    elif op == '%':
        return float(b % a)
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
    """
    Apply unary operation on the input number
    :param a: input float number
    :param op: unary operator
    :return: evaluated result number
    """
    if op == '!':
        return int(bool(not a))
    else:
        raise Exception('Invalid unary operator')


def is_commented(statement):
    """
    Check whether if the input is commented or not
    :param statement: token
    :return: boolean
    """
    statement = statement.strip()
    return statement.startswith('/*') or statement.startswith('#')


def is_op_equals(statement):
    """
    check if the token is op-equals or not
    :param statement: token input
    :return: boolean
    """
    statement = statement.replace(" ", "")
    return any((op + "=") in statement for op in (binary_operators + boolean_operators))


def is_relational_cond(statement):
    """
    check if the token is relation condition or not
    :param statement: token input
    :return: boolean
    """
    statement = statement.replace(" ", "")
    return any(op in statement for op in relational_operators)


def has_assign_var(statement):
    """
    check if its assignment operator or not
    :param statement: token input
    :return: boolean
    """
    statement = statement.replace(" ", "")
    for i in statement:
        if i.isalnum() or i == '_':
            pass
        elif i == '=':
            return True
        else:
            return False
    return False


def relational_cond_var(statement):
    """
    parse relation condition based token for evaluation
    :param statement: token input
    :return: variable and remaining token
    """
    statement = statement.replace(" ", "")
    var = ''
    i = 0
    while i < len(statement):
        if statement[i].isalnum() or statement[i] == '_':
            var += statement[i]
        elif statement[i] == '=':
            i += 1
            break
        i += 1
    return var, statement[i:]


def op_equals_var(statement):
    """
    parse token for op equal evaluation
    :param statement: token
    :return: variable
    """
    statement = statement.replace(" ", "")
    var = ''
    for i in statement:
        if i.isalnum() or i == '_':
            var += i
        else:
            return var
    return var


def new_uncommented_line(i, statements):
    """
    return next uncommented line
    :param i: current token index
    :param statements: input tokens set
    :return: new index number in input tokens
    """
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


def check_op_equals(i, tokens):
    """
    condition to check op-equals and return new index number
    :param i: current index in token
    :param tokens: token input
    :return: boolean for op-equal or not, and new index to start
    """
    if tokens[i] in binary_operators:
        return i + 1 < len(tokens) and tokens[i + 1] == '=', 2
    elif tokens[i] in boolean_operators:
        return i + 2 < len(tokens) and tokens[i + 1] == tokens[i] and tokens[i + 2] == '=', 3
    else:
        return False, 0
        # tokens[i] in (boolean_operators + binary_operators) and i + 1 < len(tokens) and tokens[i + 1] == '='


def next_varnum(index, tokens):
    """
    Checks whether next is number or variable and return if any
    :param index: current index in token
    :param tokens: token input
    :return: boolean and variable/number
    """
    if tokens[index].isdigit():
        val_str = ''
        while index < len(tokens) and tokens[index].isalnum():
            if tokens[index].isalpha(): return False, None
            val_str += tokens[index]
            index += 1
        try:
            float(val_str)
            return True, float(val_str), index
        except:
            return False, None
    elif tokens[index].isalpha():
        variable = ''
        while index < len(tokens) and (tokens[index].isalnum() or tokens[index] == '_'):
            variable += tokens[index]
            index += 1
        return True, variable, index
    return False, None


is_commented_stage = False


# Function that returns value of expression after evaluation.
def bc_evaluator(tokens):
    """
    Evaluate the token and return the result of the expression according to the precedence and extension support.
    It also takes care of comments. It takes variable value to 0.0 if not defined.
    :param tokens: token input
    :return: result of token expression
    """
    # stack to store integer values.
    values = []
    is_prev_variable = False
    is_prev_operator = True
    # stack to store operators.
    ops = []
    i = 0
    global is_commented_stage
    while i < len(tokens):
        # Current token is a whitespace, skip it.
        if tokens[i] == '#':
            break

        if tokens[i:i + 2] == '/*' and not is_commented_stage:
            is_commented_stage = True
            i += 2
            continue

        if tokens[i: i + 2] == '*/' and is_commented_stage:
            is_commented_stage = False
            i += 2
            continue

        if is_commented_stage:
            i += 1
            continue

        if tokens[i] == ' ':
            i += 1
            continue
        # Current token is an opening brace, push it to 'ops'
        elif tokens[i] == '(':
            is_prev_variable, is_prev_operator = False, True
            ops.append(tokens[i])
        # Current token is a number, push it to stack for numbers.
        elif tokens[i].isdigit():
            val_str = ''
            # There may be more than one digit in the number.
            while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                val_str += tokens[i]
                i += 1
            values.append(float(val_str))
            is_prev_variable, is_prev_operator = False, False
            i -= 1
        elif tokens[i].isalpha():
            # token is not number
            variable = ''
            while i < len(tokens) and (tokens[i].isalnum() or tokens[i] == '_'):
                variable += tokens[i]
                i += 1
            values.append(variable)
            is_prev_variable, is_prev_operator = True, False
            i -= 1
        elif tokens[i] == '-' and is_prev_operator and next_varnum(i + 1, tokens)[0]:
            ops.append(tokens[i])
            values.append(0.0)
            is_prev_variable, is_prev_operator = False, True
        # Closing brace encountered, solve entire brace.
        elif tokens[i] == ')':
            while len(ops) != 0 and ops[-1] != '(':
                op = ops.pop()
                if op in unary_operators:
                    val1 = values.pop()
                    if not is_number_(val1):
                        if val1 not in VARIABLES:
                            VARIABLES[val1] = 0.0
                        val1 = VARIABLES.get(val1)
                    values.append(apply_unary_ops(float(val1), op))
                else:
                    val2 = values.pop()
                    val1 = values.pop()
                    if not is_number_(val1):
                        if val1 not in VARIABLES:
                            VARIABLES[val1] = 0.0
                        val1 = VARIABLES.get(val1)
                    if not is_number_(val2):
                        if val2 not in VARIABLES:
                            VARIABLES[val2] = 0.0
                        val2 = VARIABLES.get(val2)
                    values.append(apply_operation(val2, val1, op))
            is_prev_variable, is_prev_operator = False, False
            ops.pop()
        elif check_op_equals(i, tokens)[0]:
            # op-equals extension
            ops.append(tokens[i])
            jump_ind = check_op_equals(i, tokens)[1]
            i += jump_ind
            is_prev_variable, is_prev_operator = False, True
            continue
        elif tokens[i] in relational_operators or (i + 1 < len(tokens) and tokens[i:i + 2] in relational_operators):
            curr_ops = tokens[i]
            if i + 1 < len(tokens) and tokens[i:i + 2] in relational_operators:
                curr_ops = tokens[i:i + 2]
                i += 1
            ops.append(curr_ops)
            is_prev_variable, is_prev_operator = False, True
            is_prev_operator = True
        elif tokens[i] in unary_operators:
            ops.append(tokens[i])
            is_prev_variable, is_prev_operator = False, True
        # Current token isf an operator.
        elif tokens[i] in (binary_operators + boolean_operators):
            # ++ / -- cases
            if (tokens[i] == '+' or tokens[i] == '-') and i + 1 < len(tokens) and tokens[i] == tokens[i + 1]:
                # if true, then post ops else pre ops
                if is_prev_variable:
                    i += 1
                    # pop last variable and do this operation
                    last_var = values.pop()
                    if last_var in VARIABLES:
                        values.append(float(VARIABLES[last_var]))
                        if tokens[i] == '+':
                            VARIABLES[last_var] += 1
                        else:
                            VARIABLES[last_var] -= 1
                    elif is_var_name(last_var):
                        VARIABLES[last_var] = 0.0
                        values.append(float(VARIABLES[last_var]))
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
                        while i < len(tokens) and (tokens[i].isalnum() or tokens[i] == '_'):
                            variable += tokens[i]
                            i += 1
                        i -= 1
                        if variable in VARIABLES:
                            if curr_ops == '+':
                                VARIABLES[variable] += 1
                                values.append(float(VARIABLES[variable]))
                            else:
                                VARIABLES[variable] -= 1
                                values.append(float(VARIABLES[variable]))
                        elif is_var_name(variable):
                            VARIABLES[variable] = 0.0
                            values.append(float(VARIABLES[variable]))
                            if tokens[i] == '+':
                                VARIABLES[variable] += 1
                            else:
                                VARIABLES[variable] -= 1
                        else:
                            raise Exception('post ++/-- can be applied to variables only')
                    else:
                        raise Exception('pre ++/-- can be applied to variables only.')
            # normal single operator case
            else:
                if i + 1 < len(tokens) and tokens[i] == tokens[i + 1]:
                    i += 1
                while len(ops) != 0 and precedence(ops[-1]) >= precedence(tokens[i]):
                    op = ops.pop()
                    if op in unary_operators:
                        val1 = values.pop()
                        if not is_number_(val1):
                            if val1 not in VARIABLES:
                                VARIABLES[val1] = 0.0
                            val1 = VARIABLES.get(val1)
                        values.append(apply_unary_ops(float(val1), op))
                    else:
                        val2 = values.pop()
                        val1 = values.pop()
                        if not is_number_(val1):
                            if val1 not in VARIABLES:
                                VARIABLES[val1] = 0.0
                            val1 = VARIABLES.get(val1)
                        if not is_number_(val2):
                            if val2 not in VARIABLES:
                                VARIABLES[val2] = 0.0
                            val2 = VARIABLES.get(val2)
                        values.append(apply_operation(val2, val1, op))
                # Push current token to 'ops'.
                ops.append(tokens[i])
            is_prev_variable, is_prev_operator = False, True
        else:
            is_prev_variable, is_prev_operator = False, True
            raise Exception('invalid')
        i += 1
    # Entire expression has been parsed at this point, apply remaining ops to remaining values.
    while len(ops) != 0:
        op = ops.pop()
        if op in unary_operators:
            val1 = values.pop()
            if not is_number_(val1):
                if val1 not in VARIABLES:
                    VARIABLES[val1] = 0.0
                val1 = VARIABLES.get(val1)
            values.append(apply_unary_ops(float(val1), op))
        else:
            val2 = values.pop()
            val1 = values.pop()
            if not is_number_(val1):
                if val1 not in VARIABLES:
                    VARIABLES[val1] = 0.0
                val1 = VARIABLES.get(val1)
            if not is_number_(val2):
                if val2 not in VARIABLES:
                    VARIABLES[val2] = 0.0
                val2 = VARIABLES.get(val2)
            values.append(apply_operation(val2, val1, op))
    # Top of 'values' contains result, return it.
    if len(values) == 0:
        return 0.0
    elif values[-1] in VARIABLES:
        return VARIABLES.get(values[-1])
    elif is_number_(values[-1]):
        return values[-1]
    else:
        return 0.0


def bc_parser(input_expression):
    """
    parse the input expression and create tokens and send each one to evaluator for evaluation. Print output as per inputs
    :param input_expression: input statements string
    """
    statements = input_expression.split('\n')
    parse_error = 0
    dbz_error = 0
    things_to_be_printed = []
    i = 0
    global is_commented_stage
    while i < len(statements):
        statement = statements[i]
        if parse_error > 0:
            break

        if is_commented_stage and '*/' not in statement:
            i += 1
            continue

        if '*/' in statement and is_commented_stage:
            index = statement.find("*/")
            is_commented_stage = False
            if index != -1:
                statement = statement[index + 2:].strip()

        if statement.strip().startswith('print'):
            # evaluate the expression(s) to be printed
            expr = statement[6:].strip().replace(' ', '')
            exprs = expr.split(',')
            values = []
            for e in exprs:
                value = ''
                try:
                    value = bc_evaluator(e)
                except ZeroDivisionError:
                    value = 'divide by zero'
                    values.append(str(value))
                    things_to_be_printed.append(' '.join(values))
                    dbz_error += 1
                    break
                except:
                    parse_error += 1
                values.append(str(value))
            if dbz_error == 0:
                things_to_be_printed.append(' '.join(values))
        elif is_commented(statement):
            i = new_uncommented_line(i, statements)
            continue
        elif is_op_equals(statement):
            try:
                var = op_equals_var(statement)
                VARIABLES[var.strip()] = bc_evaluator(statement.strip())
            except ZeroDivisionError:
                things_to_be_printed.append('divide by zero')
                dbz_error += 1
                break
            except:
                parse_error += 1
        elif is_relational_cond(statement):
            if has_assign_var(statement):
                try:
                    var, exp = relational_cond_var(statement)
                    VARIABLES[var.strip()] = bc_evaluator(exp.strip())
                except ZeroDivisionError:
                    things_to_be_printed.append('divide by zero')
                    dbz_error += 1
                except:
                    parse_error += 1
            else:
                try:
                    bc_evaluator(statement)
                except ZeroDivisionError:
                    things_to_be_printed.append('divide by zero')
                    dbz_error += 1
                except:
                    parse_error += 1
        elif '=' in statement:
            # assign a value to a variable
            var, expr = statement.split('=')
            try:
                value = bc_evaluator(expr.strip())
                VARIABLES[var.strip()] = value
            except ZeroDivisionError:
                if dbz_error == 0:
                    things_to_be_printed.append('divide by zero')
                dbz_error += 1
            except:
                parse_error += 1
        elif statement is None or len(statement) == 0:
            pass
        else:
            try:
                bc_evaluator(statement.strip())
            except ZeroDivisionError:
                if dbz_error == 0:
                    things_to_be_printed.append('divide by zero')
                dbz_error += 1
            except:
                parse_error += 1
        i += 1
    if parse_error == 0:
        for p in things_to_be_printed:
            print(p)
    else:
        print('parse error')


# main function - takes input from std in and pass it to bc parser
def bc_calculator():
    """
    takes input from stdin and send it to bc parser for evaluation of input statements
    """
    statements = sys.stdin.read()
    bc_parser(statements)


# calls main executor function which takes input from stdin and start evaluation
bc_calculator()

# ip_ = """"""
# bc_parser(ip_)
