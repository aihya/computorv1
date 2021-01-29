class Parse:
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

    def parse_side(self, string):
        degrees = dict()
        chars = list(string.replace(' ', ''))

        # Assemble numbers
        array = self.assemble_numbers(chars)

        # Collect terms
        i = 0
        while array[i]:
            if array[i] == 'X':
                try:
                    if array[i + 1] == '^':
                        degree = int(array[i + 2])
                except:
                   pass 
        

    def parse(self):
        left, right = self.equation.split('=')


class Term:
    def __init__(self, factor=0, degree=0):
        self.factor = factor
        self.degree = degree
