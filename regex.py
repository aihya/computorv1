# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regex.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #

#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/26 22:17:48 by aihya             #+#    #+#              #
#    Updated: 2021/02/27 18:14:00 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
import sys

class RegexParser:

    def __init__(self, exp):
        self.exp = exp
        self.sides = exp.split('=')
        if len(self.sides) != 2:
            print('Invalid syntax: None or many equal signs found.')
            return None
        if self.sides[0].count(' ') == len(self.sides[0]):
            print('Invalid syntax: No terms on left side.')
            return None
        if self.sides[1].count(' ') == len(self.sides[1]):
            print('Invalid syntax: No terms on right side.')
            return None

    def parse_side(self, string):
        num_grp = r"([+-]\s*|^)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*\d+|)"
        bfx_grp = r"({}\s*\*?\s*|[+-]\s*|)".format(num_grp)
        pattern = r"(\s*{}X{}\s*|\s*{}\s*)".format(bfx_grp, afx_grp, num_grp)
        m = re.findall(pattern, string)
        matches = [tup[0] for tup in m]
        return matches

    def format_err(self, terms, side):
        _ = [side]
        res = ''
        for t in terms:
            i = side.find(t)
            _ = _[-1].split(t, 1)
            if len(_[0]) != 0:
                res += '\x1b[31m{}\x1b[0m'.format(_[0])
            res += '\x1b[32m{}\x1b[0m'.format(t)
            print(_)
        if _[-1]:
            res += '\x1b[31m{}\x1b[0m'.format(_[-1])
        return res

    def print_err(self, lm, rm, sides):
        lm_formatted = self.format_err(lm, sides[0])
        rm_formatted = self.format_err(rm, sides[1])
        print('{}\x1b[32m=\x1b[0m{}'.format(lm_formatted, rm_formatted))

    def parse(self):
        lm = self.parse_side(self.sides[0])
        print('Left:\t', lm)
        rm = self.parse_side(self.sides[1])
        print('Right:\t', rm)

        
        if ''.join(lm) == self.sides[0]:
            print('Perfect match on left side')
        else:
            print('Error on left side')

        if ''.join(rm) == self.sides[1]:
            print('Perfect match on right side')
        else:
            print('Error on right side')
        self.print_err(lm, rm, self.sides)

        return lm, rm


rp = RegexParser(sys.argv[1])
if rp == None:
    exit(1)
rp.parse()
