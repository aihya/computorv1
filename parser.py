# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/20 16:20:33 by aihya             #+#    #+#              #
#    Updated: 2021/02/21 17:07:29 by aihya            ###   ########.fr        #
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

    def il(self):
        return self.i < self.l

    def spaces(self):
        while self.il() and self.exp[self.i] == ' ':
            self.i += 1

    def read_int(self):
        num = ''
        while self.il():
            if self.exp[self.i] in '0123456789':
                num += self.exp[self.i]
            self.i += 1
        if len(num) != 0:
            return int(num)
        return None

    def read_num(self):
        num = ''
        while self.il():
            if self.exp[self.i] in '.0123456789':
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
        # from beginning: 5, -+5, +5, - 5, + 5
        # in the middle: -5, +5, - 5, + 5
        #   X

        sign = 1

        self.spaces()
        if self.il() and (self.exp[self.i] == '-' or self.exp[self.i] == '+'):
            print('1.')
            self.i += 1
            if self.exp[self.i] == '-':
                print('2.')
                sign = -1
            self.spaces()
            if self.il() and self.exp[self.i] in ".0123456789":
                print('3.')
                num = self.read_num()
                if self.err == None:
                    print('4.')
                    return sign, sign * num
            else:
                print('5.')
                self.err = "Invalid token at: {}".format(self.i)
        elif self.il() and self.exp[self.i] in ".0123456789" and is_start:
            num = self.read_num()
            if self.err == None:
                return sign, sign * num
        return sign, None

    def read_degr(self, fact):
        self.spaces()
        if fact == None:
            if self.il() and self.exp[self.i] == 'X':
                self.spaces()
                if self.il() and self.exp[self.i] == '^':
                    self.spaces()
                    if self.il() and self.ex[self.i] in '.0123456789':
                        num = self.read_int()
                        
                        

    def parse(self):
        #sides = self.exp.split('=')
        #if len(sides) != 1:
        #    return self.err_msg("None or too many equal signs.")

        #while self.i < self.l:
        #    pass

        print(self.read_fact(False))
        if self.err:
            self.err_msg(self.err)


class Term:
    def __init__(self):
        self.sign = None
        self.fact = None
        self.degr = None