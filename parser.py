# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:45 by aihya             #+#    #+#              #
#    Updated: 2021/02/03 17:04:28 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time

class LexicalParser:
    def __init__(self, equation):
        self.eq = equation
        self.len = len(self.eq)
        self.terms = list()
        self.error_msg = None
        self.error = None
        self.i = 0

    def parsing_error_msg(self, pos):
        return "Parsing error at position: {}".format(pos)

    def escape_spaces(self):
        while self.i < self.len and self.eq[self.i] == ' ':
            self.i += 1

    def get_factor(self, side):
        factor = 0
        _factor = ""
        sign = 1
        if self.eq[self.i] == '-':
            sign = -1
            self.i += 1
        elif self.eq[self.i] == '+':
            self.i += 1
        self.escape_spaces()

        while self.i < self.len and self.eq[self.i] in ".0123456789":
            _factor += self.eq[self.i]
            self.i += 1

        if _factor.count('.') > 1 or len(_factor) == 0:
            self.error = True
            self.error_msg = self.parsing_error_msg(self.i - len(_factor))
            return None

        try:
            if _factor.count('.') == 0:
                factor = sign * int(_factor)
            else:
                factor = sign * float(_factor)
        except:
            self.error = True
            self.error_msg = self.parsing_error_msg(self.i - len(_factor))
            return None
        return side * sign, side * factor

    def get_degree(self):
        _degree = ""
        degree = 0
        while self.i < self.len and self.eq[self.i] == ' ':
            self.i += 1

        if self.i < self.len and self.eq[self.i] != '*':
            self.error = True
            self.error_msg = self.parsing_error_msg(self.i)
            return None

        self.i += 1
        while self.i < self.len and self.eq[self.i] == ' ':
            self.i += 1
        
        if self.i + 1 < self.len and self.eq[self.i:self.i+2] != "X^":
            self.error = True
            self.error_msg = self.parsing_error_msg(self.i - len(_degree))
            return None
        
        self.i += 2
        while self.i < self.len and self.eq[self.i] in ".0123456789":
            _degree += self.eq[self.i]
            self.i += 1
        
        if _degree.count('.') != 0 or len(_degree) == 0:
            self.error = True
            self.error_msg = self.parsing_error_msg(self.i - len(_degree))
            return None
        
        if _degree.count('.') == 0 and _degree.isnumeric():
            degree = int(_degree)
        return degree

    def get_term(self, side):
        """
            Term format:
                2.5 * X or  2.5 * X^2 or
                -5 * X  or  -5 * X^2
        """
        sign, factor = self.get_factor(side)
        if self.error:
            print(self.error_msg)
            return
        degree = self.get_degree()
        if self.error:
            print(self.error_msg)
            return
        self.terms.append(Term(sign, factor, degree))

    def parse(self):
        while self.i < self.len:
            self.escape_spaces()
            self.get_term(1)
            if self.error:
                return None
            self.escape_spaces()
            if self.eq[self.i] == '=':
                self.i += 1
                break
        while self.i < self.len:
            self.escape_spaces()
            self.get_term(-1)
            if self.error:
                return None
            self.escape_spaces()
        return self.terms

class Term:
    def __init__(self, sign=None, factor=None, degree=None):
        self.factor = factor
        self.degree = degree
        self.sign = sign

    def get_factor(self):
        return self.factor

    def get_degree(self):
        return self.degree
    
    def set_factor(self, num):
        self.factor += num
