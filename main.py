# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/20 16:20:35 by aihya             #+#    #+#              #
#    Updated: 2021/03/28 16:35:22 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from parser import Parser
from solver import Solver
import sys
import readline

usage = """Usage:
    1. python3 {} 'Expression'  : Normal mode (Evaluate expression)
    2. python3 {}               : Interactive mode
        Type 'quit' to exit from interactive mode.""".format(__file__, __file__)

if len(sys.argv[1:]) > 1:
    print(usage)
    exit(1)

if len(sys.argv[1:]) == 1:
    exp = sys.argv[1]
    terms = Parser(exp).parse()
    if terms == None:
        exit(1)
    ret = Solver(terms).solve()
    if ret:
        exit(1)
    exit(0)
else:
    count = 0
    while True:
        exp = input('\x1b[34mIn [{}]\x1b[0m: '.format(count))
        if exp.strip() == 'quit':
            exit(0)
        terms = Parser(exp).parse()
        if terms:
            Solver(terms).solve()
        count += 1
