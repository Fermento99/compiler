
# 0 is true
def negate(r):
    """ response in r """
    code = "JZERO {} 3 (negating)\n".format(r)
    code += "RESET {}\n".format(r)
    code += "JUMP 2\n"
    code += "INC {}\n".format(r)
    return code

def equal(r1, r2, h):
    """ response in r1 """
    code = "RESET {}\n".format(h)
    code += "ADD {} {}\n".format(h, r2)
    code += "SUB {} {}\n".format(h, r1)
    code += "SUB {} {}\n".format(r1, r2)
    code += "ADD {} {}\n".format(r1, h)
    return code

def notequal(r1, r2, h):
    """ response in r1 """
    code = equal(r1, r2, h)
    code += negate(r1)
    return code

def lessequal(r1, r2):
    """ response in r1 """
    code = "SUB {} {} (checking lessequal)\n".format(r1, r2)
    return code

def greater(r1, r2):
    """ response in r1 """
    code = lessequal(r1, r2)
    code += negate(r1)
    return code

def less(r1, r2):
    """ response in r2 """
    code = greaterequal(r1, r2)
    code += negate(r2)
    return code

def greaterequal(r1, r2):
    """ response in r2 """
    code = "SUB {} {} (checking greaterequal)\n".format(r2, r1)
    return code

def ifcondition(rc, condcode, commcode):
    commlen = commcode.count('\n')
    code = condcode
    code += "JZERO {} 2 (if)\n".format(rc)
    code += "JUMP {}\n".format(commlen+1)
    code += commcode
    return code

def ifelsecondition(rc, condcode, truecode, falsecode):
    truelen = truecode.count('\n')
    falselen = falsecode.count('\n')
    code = condcode
    code += "JZERO {} 2 (ifelse)\n".format(rc)
    code += "JUMP {}\n".format(truelen+2)
    code += truecode
    code += "JUMP {} (else)\n".format(falselen+1)
    code += falsecode
    return code
