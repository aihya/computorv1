# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:42 by aihya             #+#    #+#              #
#    Updated: 2021/02/15 18:34:37 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from parser import LexicalParser, Term
from solver import Solver

if len(sys.argv) == 2:
    equation = sys.argv[1]

terms = LexicalParser(equation).parse()
if terms != None:
    s = Solver(terms)
    s.reduced_form()
    s.polynomial_degree()
    s.solutions()

# "1*X^1=2*X^1" Error: Solved
# "- 8*X^1 - 5 * X^0" Error: Solved
# "X^0 +5 * X^1= 5*X^2" Error: Solved
# "5 * X^0 + 4 * X^1 = 0 * X^2" Error: Not solved

# "   5- X - X^2 - 6 * X^1= 0" Not Done.

# PGCD
