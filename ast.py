# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ast.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/15 16:14:28 by aihya             #+#    #+#              #
#    Updated: 2021/02/16 12:15:57 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Parser:
    
    def __init__(self, exp):
        self.err = None
        self.exp = exp
        self.terms = list()
        self.i = 0
        self.l = len(self.exp)

    def escape_spaces(self):
        while self.i < self.l and self.exp[self.i] == ' ':
            self.i += 1
        if self.i < self.l:
            return self.i
        return None

    def read_number(self):
        num = ""
        while self.i < self.l:
            if self.exp[self.i] not in ".0123456789":
                break
            num += self.exp[self.i]
        return num

    def read_fact(self):
        fact = self.read_number()
        if len(fact) == 0:
            return None

        dots = fact.count('.')
        if dots == 0:
            return int(fact)
        if dots == 1:
            return float(fact)

        self.err = "Invalid syntax: " + fact
        return None

    def read_degr(self):
        degr = self.read_number()
        if len(degr) == 0:
            self.err = "No degree found at " + self.i

        dots = degr.count('.')
        if dots == 0:
            return int(degr)
        self.err = "Invalid syntax: " + degr
        return None

    def read_term(self):
        if self.escape_spaces() == None:
            return None

        sign = 1
        if self.exp[self.i] == '-':
            sign = -1
        elif self.exp[self.i] == '+':
            sign = 1

        if self.escape_spaces() == None:
            return None

        fact = self.read_fact()
        if self.err != None:
            return None

        if self.escape_spaces() == None:
            return None

        if fact == None and self.exp[self.i] != 'X':
            self.err = "Invalid syntax at " + self.i
            return None

        if fact != None:
            # To reconsider !!!
            self.escape_spaces()

            if self.exp[self.i] == '*':
                # To reconsider !!!
                self.escape_spaces()

                if self.exp[self.i] == 'X':
                    # To reconsider !!!
                    self.escape_spaces()

                    if self.exp[self.i] == '^':
                        # To reconsider !!!
                        self.escape_spaces()

                        degr = self.read_degr()
			if degr == None:
			    return None
                else:
                    self.err = ""

        # In the case where fact exist, we should check if it's followed by a '*'.
        # If so, we should read degree only if 'X^' exist,
        # else if there is no '+' or '-' sign, then that's an error.
        degr = self.read_degr()

    def parse(self):
        # 1. Read terms of first member
        # 2. Check the existence of equal sign
        # 3. Read terms of second member

        while self.i < self.l:
            term = self.read_term()

class Term:

    def __init__(self):
        self.sign = None
        self.fact = None
        self.degr = None

