from parser import parser
import sys

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input = sys.argv[1]
        output = sys.argv[2]
    elif len(sys.argv) == 2:
        input = sys.argv[1]
        output = "out.mr"
    else:
        print("too few arguments")
        exit()

    i = open(input)
    data = i.read()
    i.close()
    sys.tracebacklimit = 0
    code = parser.parse(data)

    o = open(output, 'w')
    o.write(code)
    o.close()
