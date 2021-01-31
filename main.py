# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 17:55:42 by aihya             #+#    #+#              #
#    Updated: 2021/01/31 18:49:04 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from parse_equation import LexicalParser

if len(sys.argv) == 2:
    equation = sys.argv[1]

parsed_result = LexicalParser(equation).parse()
print(parsed_result)