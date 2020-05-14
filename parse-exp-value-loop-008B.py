'''
This program implements a recursive descent parser for the CFG below:

Syntax Rule  Lookahead Set          Strings generated
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → (<exp>) | <number>
'''
# Ronak Pasricha CS 341
import math

class ParseError(Exception): pass

#==============================================================
# FRONT END PARSER
#==============================================================

i = 0 # keeps track of what character we are currently reading.
err = None
# symbol tavle
table = dict()
reservedWords = {'show',"sqrt","table","cos","sin","=",'(',')','+','-','pi','/'}

#---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}


def statment ( ):
    global i, err
    if w[i] == 'table':
        print("symbol table ")
        print("--------------------")
        print("---------------------")
        i+=1
        return table
    if w[i] not in reservedWords and not w[i].isdigit():
        return id()
    if w[i] == 'show':
        i+=1
        return show()
    else:
        return exp()
def show ():
    global i, err
    rtVal = "Value: " + str(exp())
    while w[i] == ',':
        i +=1
        rtVal += ', ' + str(exp())
    return rtVal
def id ():
    global i, err
    varName = w[i]
    i+=1
    if w[i] != '=':
        return table[varName]
    i+=1
    value = exp()
    table[varName] = value
    return "done"


def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number>
#
def factor():
    global i, err
    value = None
    if w[i] == '(':
        i += 1          # read the next character
        value = exp()
        if w[i] == ')':
            i += 1
            return value
        else:
            print('missing )')
            raise ParseError
    elif w[i] == 'pi':
        return math.pi
    elif w[i] == "sin" or w[i] == "cos" or w[i] == 'sqrt':
        i +=1
        return functionExecutor(w[i-1])
    elif w[i] in table:
        i +=1
        return table[w[i-1]]
    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            print('number expected unknow symbol')
            value = None

    if value == None: raise ParseError
    return value

def functionExecutor ( token ):
    global i, err
    value = None
    rightParen = w[i]
    i+=1
    if rightParen == '(':
        expression = exp()
        leftParren = w[i]
        if leftParren == ')':
            if token == 'sqrt':
                value = math.sqrt(expression)
            elif token == 'cos':
                value = math.cos(expression)
            elif token == 'sin':
                value  = math.sin(expression)
            elif token == 'tan':
                value = math.tan(expression)
        else:
            print("missing (")
    else:
        print("missing (")
    i +=1
    return value
#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================

def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs / rhs
    else: return None

def atomic(x):
    return float(x)


w = input('\nEnter expression: ')
while w != '':
    #------------------------------
    # Split string into token list.
    #
    for c in '()+-*/':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$') # EOF marker

    i = 0


        # print("parse error ")
    try:
        print(statment())  # call the parser
    except:
        print("parse error")

    if w[i] != '$': print('Syntax error:')

    w = input('\n\nEnter expression: ')
    print()
