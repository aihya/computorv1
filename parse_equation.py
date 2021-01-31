# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parse_equation.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:45 by aihya             #+#    #+#              #
#    Updated: 2021/01/31 19:25:01 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class LexicalParser:
    def __init__(self, equation):
        self.equation = equation
        self.terms = list()
        self.error = None
        self.last_pos = 0

    def parsing_error_msg(self, pos):
        return "Parsing error at position: {}".format(pos)

    def get_factor(self, start):
        sign = 1
        factor = 0
        _factor = ""
        dot_count = 0
        l = len(self.equation)
        i = start

        # if self.equation[i] == '-':
        #     sign = -1
        #     i += 1
        #     if i < l and self.equation[i] in ".0123456789":
        #         while i < l and self.equation[i] in ".0123456789":
        #             if self.equation[i] == '.':
        #                 dot_count += 1
        #             if dot_count > 1:
        #                 self.error = self.parsing_error_msg(i)
        #                 return None
        #             _factor += self.equation[i]
        #             i += 1
        #     else:
        #         self.error = self.parsing_error_msg(i)
        #         return None

        if self.equation[i] == '-':
            sign = -1
            i += 1
        while i < l and self.equation[i] in ".0123456789":
            if self.equation[i] == '.':
                dot_count += 1
            if dot_count > 1:
                self.error = self.parsing_error_msg(i)
                return None
            _factor += self.equation[i]
            i += 1
        print(">", _factor)
        if sign == 1 and len(_factor) == 0:
            _factor = '0'
        elif dot_count > 1 and sign == -1:
            self.error = self.parsing_error_msg(i)
            return None

        self.last_pos = i
        if dot_count == 0:
            factor = sign * int(_factor)
        else:
            factor = sign * float(_factor)
        return factor
                

    def get_degree(self):
        pass

    def get_term(self, start):
        """
            Term format:
                -5 * X^2
                -5 * X
                X
        """
        # length = len(self.equation)
        # i = start
        # while i < length and self.equation[i] != '=':
        #     if self.equation[i] == '-':
        #         pass

        factor = self.get_factor(0)
        if factor == None:
            return None
        print(factor)
        
        # degree = self.get_degree()

    def parse(self):
        end = self.get_term(0)
        # while self.error == None:
        #     end = self.get_term(end)
        

class Term:
    def __init__(self, factor=None, degree=None):
        self.factor = factor
        self.degree = degree

    def get_factor(self):
        return self.factor

    def get_degree(self):
        return self.degree
