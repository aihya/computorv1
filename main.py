import sys
from parse_equation import Parser

if len(sys.argv) == 2:
    equation = sys.argv[1]

parsed_result = Parser(equation).parse()
for k in parsed_result.keys():
    for term in parsed_result[k]:
        print("{} * X^{}".format(term.get_factor(), term.get_degree()))
