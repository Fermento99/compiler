

def genconst(a, r):
    x = bin(a)[2:]
    code = "RESET {} (generating {})\n".format(r, a)
    if x[0] == '1':
        code += "INC {}\n".format(r)
    for i in range(1, len(x)):
        code += "SHL {}\n".format(r)
        if x[i] == '1':
            code += "INC {}\n".format(r)
    return code

def add(r1, r2):
    code = "ADD {} {} (adding)\n".format(r1, r2)
    return code

def subtract(r1, r2):
    code = "SUB {} {} (subtracting)\n".format(r1, r2)
    return code

def times(r1, r2, r3):
    """ response in r3 """
    code = "RESET {} (multiplying)\n".format(r3)
    code += "JODD {} 2\n".format(r1)
    code += "JUMP 2\n"
    code += "ADD {} {}\n".format(r3, r2)
    code += "SHL {}\n".format(r2)
    code += "SHR {}\n".format(r1)
    code += "JZERO {} 2\n".format(r1)
    code += "JUMP -6\n"
    return code

def divide(r1, r2, c, h, q):
    # setup
    code = "RESET {} (division setup)\n".format(q)
    code += "JZERO {} 30\n".format(r2)
    code += "RESET {}\n".format(h)
    code += "RESET {}\n".format(c)
    code += "INC {}\n".format(c)
    code += "ADD {} {}\n".format(h, r1)
    code += "JZERO {} 5\n".format(h)
    code += "INC {}\n".format(c)
    code += "SHR {}\n".format(h)
    code += "SHL {}\n".format(r2)
    code += "JUMP -4\n"
    # division
    code += "ADD {} {}\n".format(h, r1)
    code += "JZERO {} 19 (division action)\n".format(c) #jump end
    code += "DEC {}\n".format(c)
    code += "SHL {}\n".format(q)
    code += "JZERO {} -3\n".format(r1)
    code += "SUB {} {}\n".format(h, r2)
    code += "JZERO {} 5\n".format(h)
    code += "SUB {} {}\n".format(r1, r2)
    code += "INC {}\n".format(q)

    code += "SHR {}\n".format(r2)
    code += "JUMP -9\n"
    code += "ADD {} {}\n".format(h, r2)
    code += "SUB {} {}\n".format(h, r1)
    code += "JZERO {} 2\n".format(h)
    code += "JUMP 3\n"
    code += "RESET {}\n".format(r1)
    code += "JUMP -8\n"
    code += "RESET {}\n".format(h)
    code += "ADD {} {}\n".format(h, r1)
    code += "JUMP -10\n"
    return code

def reminder(r1, r2, c, h):
    # setup
    code = "JZERO {} 28 (reminder setup)\n".format(r2)
    code += "JZERO {} 28\n".format(r1)
    code += "RESET {}\n".format(h)
    code += "RESET {}\n".format(c)
    code += "INC {}\n".format(c)
    code += "ADD {} {}\n".format(h, r1)
    code += "JZERO {} 5\n".format(h)
    code += "INC {}\n".format(c)
    code += "SHR {}\n".format(h)
    code += "SHL {}\n".format(r2)
    code += "JUMP -4\n"
    # division
    code += "ADD {} {}\n".format(h, r1)
    code += "JZERO {} 17 (reminder action)\n".format(c) #jump end
    code += "DEC {}\n".format(c)
    code += "SUB {} {}\n".format(h, r2)
    code += "JZERO {} 4\n".format(h)
    code += "SUB {} {}\n".format(r1, r2)

    code += "SHR {}\n".format(r2)
    code += "JUMP -6\n"
    code += "ADD {} {}\n".format(h, r2)
    code += "SUB {} {}\n".format(h, r1)
    code += "JZERO {} 2\n".format(h)
    code += "JUMP 3\n"
    code += "RESET {}\n".format(r1)
    code += "JUMP 5\n"
    code += "RESET {}\n".format(h)
    code += "ADD {} {}\n".format(h, r1)
    code += "JUMP -10\n"
    code += "RESET {}\n".format(r1)
    return code
