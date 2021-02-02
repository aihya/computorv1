# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:42 by aihya             #+#    #+#              #
#    Updated: 2021/02/02 14:31:18 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from parse_equation import LexicalParser

if len(sys.argv) == 2:
    equation = sys.argv[1]

parsed_result = LexicalParser(equation).parse()

# "X^0 +5 * X^1= 5*X^2" ERROR