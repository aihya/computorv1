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


class RegexParser:

    def __init__(self, exp):
        self.exp = exp
        self.sides = exp.split('=', 1)

    def parse_side(self, string):
        num_grp = r"([+-]\s*|)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*([+-]\s*|)\d+|)"
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

    def show_errors(self, lm, rm, sides):
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

    def parse(self):
        err = False
        lm = self.parse_side(self.sides[0])
        print('Left:\t', lm)
        rm = self.parse_side(self.sides[1])
        print('Right:\t', rm)

        # Display whole expression with syntax errors found.
        _lm = TermsParser(lm).parsed
        _rm = TermsParser(rm).parsed
        err = self.check_side(lm, 'left') or err
        err = self.check_side(rm, 'right') or err
        err = self.show_errors(_lm, _rm, self.sides) or err

        if err:
            return None, None
        return lm, rm


class TermsParser:

    def __init__(self, terms):
        self.terms = terms
        self.parsed = self.validate()

    def term(self, term=None, valid=None):
        return {'term': term,
                'valid': valid,
                'sign': None,
                'fact': None,
                'X': False,
                'degr': None}

    def validate(self):
        _ = []
        for i, term in enumerate(self.terms):
            valid = False
            if '-' not in term and '+' not in term:
                if i != 0:
                    valid = False
                else:
                    valid = True
            else:
                valid = True
            _.append(self.term(term, valid))
        return _

    def parse(self):
        for t in self.parsed:
            if 'X' in t['term']:
                print(t['term'])


rp = RegexParser(sys.argv[1])
if rp == None:
    exit(1)
lm, rm = rp.parse()
if lm == None and rm == None:
    exit(1)
