# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/20 16:20:33 by aihya             #+#    #+#              #
#    Updated: 2021/02/23 18:20:09 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time

class Error:
    def msg(msg):
        return "Parsing error: {}".format(msg)

    def inv_tok(i):
        return "Invalid token at: {}".format(i)

class Parser:
    def __init__(self, exp):
        self.sides = self.split_exp(exp)

    def split_exp(self, exp):
        sides = exp.split('=')
        if len(sides) != 2:
            print(Error.msg("None or too many equal signs."))
            return None
        print(sides)
        return sides

    def parse(self):
        if self.sides == None:
            return None
        print("Left-hand side:")
        err, terms = Exp(self.sides[0], 1).parse()
        if err:
            print(err)

        print("Right-hand side:")
        err, terms = Exp(self.sides[1], -1).parse()
        if err:
            print(err)

class Exp:
    def __init__(self, exp, side):
        self.i = 0
        self.l = len(exp)
        self.err = None
        self.exp = exp
        self.side = side

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
        if self.il() and (self.exp[self.i] in '+-'):
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
            self.err = Error.inv_tok(self.i)
            return sign, None
        elif self.il() and self.exp[self.i] in ".0123456789" and is_start:
            num = self.read_num()
            if self.err == None:
                return sign, sign * num
        elif self.il() and is_start and self.exp[self.i] == 'X':
            return sign, None
        self.err = Error.inv_tok(self.i)
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
                    self.err = Error.inv_tok(self.i)
                    return None
            else:
                return 1
        return None

    def read_degr(self, fact, is_start):
        self.spaces()
        if fact == None:
            if is_start and self.il() and self.exp[self.i] == '*':
                self.err = Error.inv_tok(self.i)
                return None
            degr = self.read_after_X()
            return degr
        else:
            if self.il() and self.exp[self.i] == '*':
                self.i += 1
                self.spaces()
                degr = self.read_after_X()
                return degr
            elif self.il() and self.exp[self.i] not in '+-':
                self.err = Error.inv_tok(self.i)
                return None

    def parse(self):
        is_start = True

        print("[{}]".format(self.exp))

        while self.il():
            sign, fact = self.read_fact(is_start)
            print(self.i, self.l)
            if self.err:
                return Error.msg(self.err), None
            if self.il() == False:
                break
            degr = self.read_degr(fact, is_start)
            if self.err:
                return Error.msg(self.err), None
            print("sign: {} | fact: {} | degr: {}".format(sign, fact, degr))
            is_start = False
        return None, None
            

class Term:
    def __init__(self):
        self.sign = None
        self.fact = None
        self.degr = None