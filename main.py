# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:42 by aihya             #+#    #+#              #
#    Updated: 2021/02/03 16:26:52 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from parser import LexicalParser, Term
from solver import Solver

if len(sys.argv) == 2:
    equation = sys.argv[1]

terms = LexicalParser(equation).parse()
s = Solver(terms)
s.reduced_form()
s.polynomial_degree()
s.solutions()

# "- 8*X^1 - 5 * X^0" Error: Not solved
# "X^0 +5 * X^1= 5*X^2" Error: Solved

