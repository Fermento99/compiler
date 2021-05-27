import ply.lex as lex

tokens = (
    "PID",
    "NUM",
    "DECLARE",
    "BEGIN",
    "END",
    "LPAR",
    "RPAR",
    "COLON",
    "SEMICOLON",
    "ASSIGN",
    "IF",
    "THEN",
    "ELSE",
    "ENDIF",
    "WHILE",
    "DO",
    "ENDWHILE",
    "REPEAT",
    "UNTIL",
    "FOR",
    "FROM",
    "TO",
    "DOWNTO",
    "ENDFOR",
    "READ",
    "WRITE",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "REMINDER",
    "EQ",
    "NEQ",
    "GT",
    "GEQ",
    "LT",
    "LEQ",
    "COMMA",
)

t_ignore_COMMENT = r'\[(.|\n)*?\]'
t_ignore = " \t\n"
t_DECLARE = r'DECLARE'
t_BEGIN = r'BEGIN'
t_END = r'END'
t_LPAR = "\("
t_RPAR = "\)"
t_COLON = ":"
t_SEMICOLON = ";"
t_ASSIGN = ":="
t_IF = "IF"
t_THEN = "THEN"
t_ELSE = "ELSE"
t_ENDIF = "ENDIF"
t_WHILE = "WHILE"
t_DO = "DO"
t_ENDWHILE = "ENDWHILE"
t_REPEAT = "REPEAT"
t_UNTIL = "UNTIL"
t_FOR = "FOR"
t_FROM = "FROM"
t_TO = "TO"
t_DOWNTO = "DOWNTO"
t_ENDFOR = "ENDFOR"
t_READ = "READ"
t_WRITE = "WRITE"
t_PLUS = "\+"
t_MINUS = "-"
t_TIMES = "\*"
t_DIVIDE = "/"
t_REMINDER = "%"
t_EQ = "="
t_NEQ = "!="
t_GT = ">"
t_GEQ = ">="
t_LT = "<"
t_LEQ = "<="
t_COMMA = ","
t_PID = r'[_a-z]+'

def t_error(t):
    pass


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

lexer = lex.lex()

# f = open("./labor4/error1.imp")
# data = f.read()
# f.close()

# lexer.input(data)
#
# while(True):
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
