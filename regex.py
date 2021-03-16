# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regex.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:15:14 by aihya             #+#    #+#              #
#    Updated: 2021/03/16 14:58:21 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
import sys

class Parser:

    def __init__(self, exp):
        self.exp = exp
        self.sides = exp.split('=', 1)
        self.l_terms = None
        self.r_terms = None
        self.err = False
        self.errmsgs = []

    def extract_terms(self, string):
        num_grp = r"([+-]\s*|)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*{}|)".format(num_grp)
        bfx_grp = r"(\s*{}\s*\*?\s*|\s*[+-]\s*|)".format(num_grp)
        pattern = r"(\s*{}X{}\s*|\s*{}\s*)".format(bfx_grp,
                                                   afx_grp, num_grp)
        m = re.findall(pattern, string)
        matches = [tup[0] for tup in m]
        return matches

    def term_obj(self, term, sign, fact, degr, X):
        return {
            'term': term,
            'sign': sign,
            'fact': fact,
            'degr': degr,
            'X': X
        }

    def is_empty(self, string):
        _is_empty = True
        for c in string:
            if c == ' ':
                continue
            _is_empty = False
            break
        return _is_empty

    def format_err(self, terms, side):
        res = ''

        if terms:
            for i, term in enumerate(terms):
                splitted = side.split(term, 1)
                if splitted[0]:
                    res += '\x1b[1;4;31m{}\x1b[0m'.format(splitted[0])
                if i != 0 and not self.is_sign_preceded(i, term):
                    res += '\x1b[1;4;31m{}\x1b[0m'.format(term)
                else:
                    res += '\x1b[32m{}\x1b[0m'.format(term)
                side = splitted[-1]
            res += '\x1b[1;4;31m{}\x1b[0m'.format(splitted[-1])
        else:
            res += '\x1b[1;4;31m{}\x1b[0m'.format(side)
        return res
        
    def show_exp(self):
        res = ''
        if len(self.sides) == 2:
            lres = self.format_err(self.l_terms, self.sides[0])
            rres = self.format_err(self.r_terms, self.sides[1])
            res = '{}\x1b[32m=\x1b[0m{}'.format(lres, rres)
        elif len(self.sides) == 1:
            lres = self.format_err(self.l_terms, self.sides[0])
            if not self.is_empty(self.sides[0]):
                res = '{}\x1b[32m= 0\x1b[0m'.format(lres)
            else:
                res = '{}\x1b[32m\x1b[0m'.format(lres)
        print('Expression: [{}]'.format(res))

    # Terms parsing functions ##################################################

    def is_sign_preceded(self, i, term):
        sign_match = re.match(r'^\s*[+-]', term)
        if i != 0 and sign_match == None:
            return False
        return True

    def parse_terms(self, terms):
        pass
    ############################################################################

    def parse(self):
        if len(self.sides) == 2:
            if self.is_empty(self.sides[0]):
                self.err = True
                self.errmsgs.append('Empty left side')
            else:
                self.l_terms = self.extract_terms(self.sides[0])
                print(self.l_terms)        
            if self.is_empty(self.sides[1]):
                self.err = True
                self.errmsgs.append('Empty right side')
            else:
                self.r_terms = self.extract_terms(self.sides[1])
                print(self.r_terms)
        elif len(self.sides) == 1:
            if not self.is_empty(self.sides[0]):
                self.l_terms = self.extract_terms(self.sides[0])
            else:
                self.err = True
                self.errmsgs.append('Expression is empty')
        
        self.show_exp()
        if self.err:
            for err in self.errmsgs:
                print('Error: {}'.format(err))

        return self.l_terms, self.r_terms

parser = Parser(sys.argv[1])
if parser == None:
    exit(1)
lm, rm = parser.parse()
if lm == None and rm == None:
    exit(1)
