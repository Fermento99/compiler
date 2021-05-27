import maths


def while_loop(r, cond, comm):
    condl = cond.count('\n')
    comml = comm.count('\n')
    code = cond
    code += "JZERO {} 2 (while loop)\n".format(r)
    code += "JUMP {}\n".format(comml+2)
    code += comm
    code += "JUMP -{}\n".format(comml+2+condl)
    return code

def repeat_loop(r, cond, comm):
    condl = cond.count('\n')
    comml = comm.count('\n')
    code = comm
    code += cond
    code += "JZERO {} 2 (repeat loop)\n".format(r)
    code += "JUMP -{}\n".format(1 + comml + condl)
    return code

def for_up_loop(mic, mpr, f, l):
    code = maths.genconst(mic, mpr)
    code += "STORE {} {} (for loop init)\n".format(f, mpr)
    code += "INC {}\n".format(mpr)
    code += "STORE {} {}\n".format(l, mpr)
    code += "SUB {} {}\n".format(f, l)
    code += "JZERO {} 2\n".format(f)
    # this needs jump but dont know how much yet

    itr = maths.genconst(mic, mpr)
    itr += "LOAD {} {} (for loop iteration)\n".format(f, mpr)
    itr += "INC {}\n".format(f)
    itr += "STORE {} {}\n".format(f, mpr)
    itr += "INC {}\n".format(mpr)
    itr += "LOAD {} {}\n".format(l, mpr)
    itr += "SUB {} {}\n".format(f, l)
    itr += "JZERO {} ".format(f)
    return code, itr


def for_down_loop(mic, mpr, f, l):
    code = maths.genconst(mic, mpr)
    code += "STORE {} {} (for loop init)\n".format(f, mpr)
    code += "INC {}\n".format(mpr)
    code += "STORE {} {}\n".format(l, mpr)
    code += "SUB {} {}\n".format(l, f)
    code += "JZERO {} 2\n".format(l)
    # this needs jzero but dont know how much yet

    itr = maths.genconst(mic, mpr)
    itr += "LOAD {} {} (for loop iteration)\n".format(f, mpr)
    itr += "JZERO {} 7\n".format(f)
    itr += "DEC {}\n".format(f)
    itr += "STORE {} {}\n".format(f, mpr)
    itr += "INC {}\n".format(mpr)
    itr += "LOAD {} {}\n".format(l, mpr)
    itr += "SUB {} {}\n".format(l, f)
    itr += "JZERO {} ".format(l)
    return code, itr

def for_loop(desc, comm, itr):
    commlen = comm.count('\n')
    desclen = desc.count('\n')
    itrlen = itr.count('\n')
    code = desc
    code += "JUMP {}\n".format(commlen + itrlen + 2)
    code += comm
    code += itr
    code += "-{}\n".format(itrlen + commlen + 2)
    return code
