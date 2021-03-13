# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regex.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:15:14 by aihya             #+#    #+#              #
#    Updated: 2021/03/01 19:00:02 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
import sys


class Parser:

    def __init__(self, exp):
        self.exp = exp
        self.sides = exp.split('=', 1)

    def extract_terms(self, string):
        num_grp = r"([+-]\s*|)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*([+-]?\s*|)\d+|)"
        bfx_grp = r"(\s*{}\s*\*?\s*|\s*[+-]\s*|)".format(num_grp)
        pattern = r"(\s*{}X{}\s*|\s*{}\s*)".format(bfx_grp,
                                                   afx_grp, num_grp)
        m = re.findall(pattern, string)
        matches = [tup[0] for tup in m]
        return matches

    def format_err(self, terms, side):
        _ = [side]
        res = ''
        err = False
        for t in terms:
            _ = _[-1].split(t['term'], 1)
            if len(_[0]) != 0:
                res += '\x1b[1;31m{}\x1b[0m'.format(_[0])
                err = True
            if t['valid'] == False:
                res += '\x1b[1;31m{}\x1b[0m'.format(t['term'])
                err = True
            else:
                res += '\x1b[32m{}\x1b[0m'.format(t['term'])
        if _[-1]:
            res += '\x1b[1;31m{}\x1b[0m'.format(_[-1])
            err = True
        return res, err

    def show_exp(self, lm, rm, sides):
        lm_formatted, _ = self.format_err(lm, sides[0])
        err = _
        rm_formatted, _ = self.format_err(rm, sides[1])
        err = err or _
        print('{}\x1b[32m=\x1b[0m{}'.format(lm_formatted, rm_formatted))
        return err

    def is_empty(self, string):
        _is_empty = True
        for c in string:
            if c == ' ':
                continue
            _is_empty = False
            break
        return _is_empty

    def check_side(self, terms, side_name):
        err = False
        i = 0 if side_name == 'left' else 1
        joined = ''.join(terms)
        if self.is_empty(joined):
            print('Invalid syntax: No terms in {} side.'.format(side_name))
            err = err or True
        elif joined != self.sides[i]:
            print('Invalid syntax.')
            err = err or True
        return err

    def reduce(self, terms):
        pass

    def parse(self):

        lm = self.extract_terms(self.sides[0])
        print('Left:\t', lm)


        # Bonus. No right side: (ex: 5 * X^2 + 6X - 10)

        rm = self.extract_terms(self.sides[1])
        print('Right:\t', rm)

        print('\nParsing lm_terms:')
        lm_terms = TermsParser(lm, self.sides[0])
        print('\nParsing rm_terms:\n')
        rm_terms = TermsParser(rm, self.sides[1])

        _lm = lm_terms.terms
        _rm = rm_terms.terms

        if self.check_side(lm, 'left') or self.check_side(rm, 'right'):
            self.show_exp(_lm, _rm, self.sides)
            return None, None
        self.show_exp(_lm, _rm, self.sides)

        return lm, rm


class TermsParser:

    def __init__(self, terms, side):
        self.terms = self.parse(terms)
        self.side = side

    def term(self):
        return {'term': None,
                'valid': False,
                'sign': None,
                'fact': None,
                'X': False,
                'degr': None}

    def is_valid(self, term, i):
        valid = True
        match = re.findall(r'^\s*[+-]', term)
        if not match:
            valid = False if i != 0 else True
            valid = valid or self.side.find(term) == 0
        else:
            valid = True
        return valid

    def conv_num(self, s):
        if s is not None:
            if '.' in s:
                return float(s.replace(' ', ''))
            return int(s.replace(' ', ''))
        return None

    def parse(self, terms):
        num_regex = r'(([+-]\s*|)\d+(\.\d+|))'
        _ = []
        for i, t in enumerate(terms):
            term = self.term()
            term['term'] = t
            term['valid'] = self.is_valid(t, i)
            if 'X' in t:
                xl, xr = t.split('X')

                fact_match = re.search(num_regex, xl)
                degr_match = re.search(num_regex, xr)
                
                fact = fact_match.group() if fact_match else None
                degr = degr_match.group() if degr_match else None

                term['fact'] = self.conv_num(fact)
                term['degr'] = self.conv_num(degr)
                term['X'] = True
            else:
                fact = t
                degr = None

                term['fact'] = self.conv_num(fact)
            term['sign'] = -1 if fact and '-' in fact else 1
            print("{} | {} | {} | {} | {}".format(term['term'], term['sign'], term['fact'], term['degr'], term['X']))
            _.append(term)
        
        return _

parser = Parser(sys.argv[1])
if parser == None:
    exit(1)
lm, rm = parser.parse()
if lm == None and rm == None:
    exit(1)
