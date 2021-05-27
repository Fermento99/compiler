

def from_memory(mir, r):
    """ response in r """
    code = "LOAD {} {} (loading from memory)\n".format(r, mir)
    return code

def to_memory(mir, vr):
    """saves value of vr in mir p"""
    code = "STORE {} {} (storing in memory)\n".format(vr, mir)
    return code

def print_output(r, h):
    code = "RESET {} (printing)\n".format(h)
    code += "STORE {} {}\n".format(r, h)
    code += "PUT {}\n".format(h)
    return code

def read_input(r):
    code = "GET {} (reading)\n".format(r)
    return code
