# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/20 16:20:33 by aihya             #+#    #+#              #
#    Updated: 2021/02/22 17:24:46 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Parser:
    def __init__(self, exp):
        self.exp = exp
        self.l = len(exp)
        self.i = 0
        self.err = None

    def err_msg(self, msg):
        print("Parsing error:", msg)
        return None

    def inv_tok(self):
        return "Invalid token at: {}".format(self.i)

    def il(self):
        return self.i < self.l

    def spaces(self):
        while self.il() and self.exp[self.i] == ' ':
            self.i += 1

    def read_int(self):
        num = ''
        while self.il() and self.exp[self.i] in '0123456789':
            num += self.exp[self.i]
            self.i += 1
        if len(num) != 0:
            return int(num)
        return None

    def read_num(self):
        num = ''
        while self.il() and self.exp[self.i] in '.0123456789':
            num += self.exp[self.i]
            self.i += 1
        dots = num.count('.')
        if dots > 1:
            self.err = "Invalid syntax: {}".format(num)
            return None
        if dots == 1:
            return float(num)
        return int(num)

    def read_fact(self, is_start):
        sign = 1

        self.spaces()
        if self.il() and (self.exp[self.i] == '-' or self.exp[self.i] == '+'):
            if self.il() and self.exp[self.i] == '-':
                sign = -1
            self.i += 1
            self.spaces()
            if self.il() and self.exp[self.i] in ".0123456789":
                num = self.read_num()
                if self.err == None:
                    return sign, sign * num
            elif self.il() and self.exp[self.i] == 'X':
                return sign, None
            else:
                self.err = self.inv_tok()
                return sign, None

        elif self.il() and self.exp[self.i] in ".0123456789" and is_start:
            num = self.read_num()
            if self.err == None:
                return sign, sign * num
        return sign, None

    def read_after_X(self):
        if self.il() and self.exp[self.i] == 'X':
            self.i += 1
            self.spaces()
            if self.il() and self.exp[self.i] == '^':
                self.i += 1
                self.spaces()
                if self.il() and self.exp[self.i] in '0123456789':
                    degr = self.read_int()
                    return degr
                else:
                    self.err = self.inv_tok()
                    return None
            else:
                return 1

    def read_degr(self, fact):
        self.spaces()
        if fact == None:
            degr = self.read_after_X()
            return degr
        else:
            if self.il() and self.exp[self.i] == '*':
                self.i += 1
                self.spaces()
                degr = self.read_after_X()
                return degr
            elif self.exp[self.i] not in '+-':
                self.err = self.inv_tok()
                return None

    def parse(self):
        #sides = self.exp.split('=')
        #if len(sides) != 1:
        #    return self.err_msg("None or too many equal signs.")

        start = True
        while self.il():

            print("i:", self.i)
            sign, fact = self.read_fact(start)
            if self.err:
                self.err_msg(self.err)
                return None
            degr = self.read_degr(fact)
            if self.err:
                self.err_msg(self.err)
                return None
            print("sign: {} | fact: {} | degr: {}".format(sign, fact, degr))
            start = False


class Term:
    def __init__(self):
        self.sign = None
        self.fact = None
        self.degr = None