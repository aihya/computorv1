# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regex.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:15:14 by aihya             #+#    #+#              #
#    Updated: 2021/03/17 16:00:06 by aihya            ###   ########.fr        #
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
        self.terms = []

    def extract_terms(self, string):
        num_grp = r"([+-]\s*|)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*{}|)".format(num_grp)
        bfx_grp = r"(\s*{}\s*\*?\s*|\s*[+-]\s*|)".format(num_grp)
        pattern = r"(\s*{}X{}\s*|\s*{}\s*)".format(bfx_grp,
                                                   afx_grp, num_grp)
        m = re.findall(pattern, string)
        matches = [tup[0] for tup in m]
        return matches

    def term_obj(self, term=None, sign=None, fact=None, degr=None, X=None):
        return {
            'term': term,
            'sign': sign,
            'fact': fact,
            'degr': degr,
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
        print('Expression: \x1b[38;5;240m[\x1b[0m{}\x1b[38;5;240m]\x1b[0m'.format(res))

    

    # Terms parsing functions ##################################################

    def conv_num(self, num):
        return float(num) if '.' in num else int(num)

    def is_sign_preceded(self, i, term):
        sign_match = re.match(r'^\s*[+-]', term)
        if i != 0 and sign_match == None:
            return False
        return True

    def nospace(self, string):
        return string.replace(' ', '')

    def parse_term(self, term):
        # Parse each term individually
        
        t = self.term_obj()
        t['term'] = term
        if 'X' in term:

            bfx = re.search(r'^\s*(([+-]\s*|)\d+(\.\d+|))', term)
            if bfx:
                # print(bfx.groups())
                bfx = self.nospace(bfx.groups()[0])

            afx = re.search(r"\^\s*(([+-]\s*|)\d+(\.\d+|))", term)
            if afx:
                # print(afx.groups())
                afx = self.nospace(afx.groups()[0])

            t['fact'] = self.conv_num(bfx) if bfx else None
            t['degr'] = self.conv_num(afx) if afx else None

        else:
            t['fact'] = self.conv_num(self.nospace(term))
        
        sign = re.search(r'^\s*([+-])', term)
        if sign:
            _ = sign.groups()[0]
            t['sign'] = -1 if _ == '-' else 1
        else:
            t['sign'] = 1

        print(t['term'], '\t', t['sign'], t['fact'], t['degr'])
    ############################################################################

    def parse(self):
        # Terms extraction.
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
                self.r_terms = ['0']
            else:
                self.err = True
                self.errmsgs.append('Expression is empty')
        # End: Terms extraction.

        self.show_exp()
        if self.err:
            for err in self.errmsgs:
                print('Error: {}'.format(err))
            return None, None

        for t in self.l_terms:
            self.parse_term(t)
        
        

        return self.l_terms, self.r_terms

parser = Parser(sys.argv[1])
if parser == None:
    exit(1)
lm, rm = parser.parse()
if lm == None and rm == None:
    exit(1)
