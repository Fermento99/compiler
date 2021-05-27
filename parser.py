import ply.yacc as yacc
from lexer import tokens, lexer
from memory import Memory
import operations
import maths
import conditions
import loops


# registers
registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, }
mem = Memory()

def print_registers():
    for i in registers.values():
        if i == 0:
            i = '.'
        else:
            i = '#'
        print(i, ' ', end ='')
    print("  \t", end='')

def get_register(fname):
    for i in registers.keys():
        if registers[i] == 0:
            registers[i] = 1
            # print_registers()
            # print("requested {} register by '{}'".format(i, fname))
            return i
    raise Exception("No free registers for {}".format(fname))

def release_register(r, fname):
    registers[r] = 0
    # print_registers()
    # print("register {} relesed by '{}'".format(r, fname))


# Parser
#######################################################
start = 'program'

def p_program_declare(p):
    'program : DECLARE declarations BEGIN commands END'
    p[0] = p[4] + "HALT\n"

def p_program(p):
    'program : BEGIN commands END'
    p[0] = p[2] + "HALT\n"



# declarations
def p_declarations_var(p):
    'declarations : declarations COMMA PID'
    if not mem.add_var(p[3]):
        raise(Exception("reinicialization of variable '{}'".format(p[3])))

def p_declaration_var(p):
    'declarations : PID'
    if not mem.add_var(p[1]):
        raise(Exception("reinicialization of variable '{}'".format(p[1])))


def p_declaration_arr(p):
    'declarations : PID LPAR NUM COLON NUM RPAR'
    if p[3] > p[5]:
        raise(Exception("bad tab declaration '{}'".format(p[1])))
    if not mem.add_tab(p[1], p[3], p[5]):
        raise(Exception("redeclaration of variable '{}'".format(p[1])))

def p_declarations_arr(p):
    'declarations : declarations COMMA PID LPAR NUM COLON NUM RPAR'
    if p[5] > p[7]:
        raise(Exception("bad tab declaration '{}', (start cannot be smaller than end)".format(p[3])))
    if not mem.add_tab(p[3], p[5], p[7]):
        raise(Exception("redeclaration of variable '{}'".format(v)))


# commands
def p_commands(p):
    '''commands : commands command
                | command'''
    p[0] = ''.join(p[1:])

def p_command_if(p):
    'command : IF condition THEN commands ENDIF'
    r, condcom = p[2]
    comm = p[4]
    code = conditions.ifcondition(r, condcom, comm)
    # release_register(r, "if")
    p[0] = code

def p_command_ifelse(p):
    'command : IF condition THEN commands ELSE commands ENDIF'
    r, condcom = p[2]
    tcode = p[4]
    fcode = p[6]
    code = conditions.ifelsecondition(r, condcom, tcode, fcode)
    # release_register(r, 'ifelse')
    p[0] = code

def p_command_while(p):
    'command : WHILE condition DO commands ENDWHILE'
    r, cond = p[2]
    comm = p[4]
    # release_register(r, 'while')
    code = loops.while_loop(r, cond, comm)
    p[0] = code

def p_command_repeat(p):
    'command : REPEAT commands UNTIL condition SEMICOLON'
    r, cond = p[4]
    comm = p[2]
    # release_register(r, 'repeat')
    code = loops.repeat_loop(r, cond, comm)
    p[0] = code

def p_command_for(p):
    'command : FOR fordescription DO commands ENDFOR'
    desc, itr, var = p[2]
    comm = p[4]
    mem.rm_var(var)
    mem.rm_var(var + '1')
    p[0] = loops.for_loop(desc, comm, itr)

def p_fordescription(p):
    '''fordescription : PID FROM value DOWNTO value
                      | PID FROM value TO value'''
    var = p[1]
    r1, c1 = p[3]
    r2, c2 = p[5]
    if not mem.add_var(var):
        raise(Exception("reinicialization of variable '{}' in for loop".format(var)))
    mem.initialize_var(var)
    mem.add_var(var + '1')
    mem.initialize_var(var + '1')
    mic = mem.get_var(var)
    mir = get_register("forloop")
    if p[4] == 'DOWNTO':
        code, itr = loops.for_down_loop(mic, mir, r1, r2)
    else:
        code, itr = loops.for_up_loop(mic, mir, r1, r2)
    release_register(r1, "forloop")
    release_register(r2, "forloop")
    release_register(mir, "forloop")
    p[0] = c1 + c2 + code, itr, var


def p_command_read(p):
    'command : READ identifier SEMICOLON'
    ri, ci, var = p[2]
    if var:
        mem.initialize_var(var)
    code = operations.read_input(ri)
    release_register(ri, "read")
    p[0] = ci + code

def p_command_write(p):
    'command : WRITE value SEMICOLON'
    r1, c1 = p[2]
    h = get_register("write")
    code = operations.print_output(r1, h)
    release_register(r1, "write")
    release_register(h, "write")
    p[0] = c1 + code

def p_command_assign(p):
    'command : identifier ASSIGN expression SEMICOLON'
    ri, ci, var = p[1]
    re, ce = p[3]
    if var:
        mem.initialize_var(var)
    code = operations.to_memory(ri, re)
    release_register(ri, "assign")
    release_register(re, "assign")
    p[0] = ci + ce + code


# expressions
def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

def p_expression_add(p):
    'expression : value PLUS value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = maths.add(r1, r2)
    release_register(r2, "add")
    p[0] = r1, c1 + c2 + code

def p_expression_subtract(p):
    'expression : value MINUS value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = maths.subtract(r1, r2)
    release_register(r2, "subtract")
    p[0] = r1, c1 + c2 + code

def p_expression_multiply(p):
    'expression : value TIMES value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    h = get_register("multiply")
    code = maths.times(r1, r2, h)
    release_register(r1, "multiply")
    release_register(r2, "multiply")
    p[0] = h, c1 + c2 + code

def p_expression_divide(p):
    'expression : value DIVIDE value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    c = get_register("divide")
    h = get_register("divide")
    q = get_register("divide")
    code = maths.divide(r1, r2, c, h, q)
    release_register(r1, "divide")
    release_register(r2, "divide")
    release_register(c, "divide")
    release_register(h, "divide")
    p[0] = q, c1 + c2 + code

def p_expression_reminder(p):
    'expression : value REMINDER value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    c = get_register("reminder")
    h = get_register("reminder")
    code = maths.reminder(r1, r2, c, h)
    release_register(r2, "reminder")
    release_register(c, "reminder")
    release_register(h, "reminder")
    p[0] = r1, c1 + c2 + code


# conditions
def p_condition_eq(p):
    'condition : value EQ value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    h = get_register("equals")
    code = conditions.equal(r1, r2, h)
    release_register(r1, "eq")
    release_register(r2, "eq")
    release_register(h, "eq")
    p[0] = r1, c1 + c2 + code

def p_condition_neq(p):
    'condition : value NEQ value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    h = get_register("neq")
    code = conditions.notequal(r1, r2, h)
    release_register(r1, "neq")
    release_register(r2, "neq")
    release_register(h, "neq")
    p[0] = r1, c1 + c2 + code

def p_condition_geq(p):
    'condition : value GEQ value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = conditions.greaterequal(r1, r2)
    release_register(r1, "geq")
    release_register(r2, "geq")
    p[0] = r2, c1 + c2 + code

def p_condition_gt(p):
    'condition : value GT value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = conditions.greater(r1, r2)
    release_register(r2, "gt")
    release_register(r1, "gt")
    p[0] = r1, c1 + c2 + code

def p_condition_leq(p):
    'condition : value LEQ value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = conditions.lessequal(r1, r2)
    release_register(r2, "leq")
    release_register(r1, "leq")
    p[0] = r1, c1 + c2 + code

def p_condition_lt(p):
    'condition : value LT value'
    r1, c1 = p[1]
    r2, c2 = p[3]
    code = conditions.greater(r2, r1)
    release_register(r1, "lt")
    release_register(r2, "lt")
    p[0] = r2, c1 + c2 + code


# values
def p_value_const(p):
    'value : NUM'
    r = get_register("value: const")
    p[0] = r, maths.genconst(p[1], r)

def p_value_var(p):
    'value : identifier'
    mr, lastcode, v = p[1]
    if v:
        if not mem.check_var(v):
            raise Exception("using uninitialized variable '{}'".format(v))
    r = get_register("value: var")
    code = operations.from_memory(mr, r)
    release_register(mr, "value: id")
    p[0] = r, lastcode + code

# identifier
def p_identifier_var(p):
    'identifier : PID'
    index = mem.get_var(p[1])
    if index == -1:
        raise(Exception("using not declared variable '{}'".format(p[1])))
    if index == -2:
        raise(Exception("trying to use variable like array ('{}')".format(p[1])))

    r = get_register("id: var")
    code = maths.genconst(index, r)
    p[0] = r, code, p[1]

def p_identifier_tabvar(p):
    'identifier : PID LPAR PID RPAR'
    vari = mem.get_var(p[3])
    tabi, fi = mem.get_tab_var(p[1])
    if vari == -1:
        raise(Exception("using not declared variable '{}'".format(p[1])))
    if vari == -2:
        raise(Exception("trying to use variable like array ('{}')".format(p[1])))

    r1 = get_register("id: tabv")
    r2 = get_register("id: tabv")
    c1 = maths.genconst(vari, r1)
    c2 = operations.from_memory(r1, r2)
    c3 = maths.genconst(fi, r1)
    c4 = maths.subtract(r2, r1)
    c5 = maths.genconst(tabi, r1)
    c6 = maths.add(r2, r1)

    release_register(r1, "id: tabv")

    p[0] = r2, c1 + c2 + c3 + c4 + c5 + c6, False

def p_identifier_tabconst(p):
    'identifier : PID LPAR NUM RPAR'
    index = mem.get_tab(p[1], p[3])
    if index == -1:
        raise(Exception("using not declared variable '{}'".format(p[1])))
    if index == -2:
        raise(Exception("trying to use variable like array ('{}')".format(p[1])))

    r = get_register("id: tabc")
    code = maths.genconst(index, r)
    p[0] = r, code, False

# errors
def p_error(p):
    raise Exception("Some Error")

def p_declaration_err(p):
    '''declarations : declarations COMMA PID NUM
                    | PID NUM
                    | declarations COMMA NUM PID
                    | NUM PID NUM'''
    if p[2] == "COMMA":
        v = str(p[3]) + str(p[4])
    else:
        v = str(p[1]) + str(p[2])
    raise Exception("wrong variable declaration '{}'".format(v))



parser = yacc.yacc()
