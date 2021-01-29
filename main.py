import sys
from parse_equation import Parse

if len(sys.argv) == 2:
    equation = sys.argv[1]

#parsed_result = Parse(equation)

equation = equation.replace(' ', '')
s = list(equation)
res = list()
n = ''
for c in s:
    if c in '.0123456789':
        n += c
        continue
    else:
        if len(n) != 0:
            res.append(n)
            n = ''
        res.append(c)
if len(n) != 0:
    res.append(n)

print(res)
