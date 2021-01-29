class Parser:
    def __init__(self, equation):
        self.equation = equation
        self.terms = list()

    def assemble_numbers(self, chars):
        res = list()
        number = ''
        for c in chars:
            if c in '.0123456789':
                number += c
                continue
            else:
                if len(number) != 0:
                    res.append(number)
                    number = ''
                res.append(c)
        if len(number) != 0:
            res.append(number)

        return res

    def convert_num(self, num):
        count = num.count('.')
        return int(num) if count == 0 else float(num)

    def parse_side(self, string):
        degrees = dict()
        chars = list(string.replace(' ', ''))

        # Assemble numbers
        array = self.assemble_numbers(chars)
        length = len(array)

        # Collect terms
        i = 0
        while i < length:
            if array[i] == 'X':
                if i + 1 < length:
                    if array[i + 1] == '^':
                        degree = self.convert_num(array[i + 2])
                    else:
                        degree = 1
                if i - 1 >= 0:
                    if array[i - 1] == '*':
                        factor = self.convert_num(array[i - 2])
                    else:
                        factor = 1
                    if i - 3 >= 0:
                        if array[i - 3] == '-':
                            factor *= -1
                term = Term(factor=factor, degree=degree)
                if degrees.get(degree) == None:
                    degrees[degree] = list()
                degrees[degree].append(term)
            i += 1
        return degrees

    def parse(self):
        left, right = self.equation.split('=')
        return self.parse_side(left)


class Term:
    def __init__(self, factor=None, degree=None):
        self.factor = factor
        self.degree = degree

    def get_factor(self):
        return self.factor

    def get_degree(self):
        return self.degree
