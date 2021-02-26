# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regex.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/26 22:17:48 by aihya             #+#    #+#              #
#    Updated: 2021/02/27 00:26:45 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re


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
        pattern = r"(((^\d+|[+-] *\d+)(\.?\d+|) *\*? *|[+-]? *)X( *\^ *[+-]?\d+|)|((\d+|[+-] *\d+)(\.?\d+|)))"
        m = re.findall(pattern, string, flags=0)
        matches = [tup[0] for tup in m]
        return matches

    def parse(self):
        lm = self.parse_side(self.sides[0])
        print(lm)
        rm = self.parse_side(self.sides[1])
        print(rm)
        return lm, rm


res = RegexParser(
    ' 5  - X^  5 -  7-5*X^3 = -X - 13 37.42 +\t1337.42 -5X -X')
if res == None:
    print("poop")
    exit(1)
res.parse()
