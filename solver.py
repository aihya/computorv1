# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    solver.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/02 16:56:21 by aihya             #+#    #+#              #
#    Updated: 2021/02/02 18:16:19 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections import OrderedDict

class Solver:
    def __init__(self, terms):
        self.terms = terms
        self.degrees = dict()
    
    def solve(self):
        pass

    def abs(self, n):
        if n < 0:
            return n * -1
        return n

    def reduced_form(self):
        non_zero = False
        is_start = True

        for term in self.terms:
            if term.degree in self.degrees:
                self.degrees[term.degree] += term.factor
            else:
                self.degrees[term.degree] = term.factor
        sorted_degrees = sorted(self.degrees)
        print("Reduced form: ", end='')
        for d in sorted_degrees:
            if self.degrees[d] != 0:
                if self.degrees[d] < 0:
                    if is_start:
                        print("-", end='')
                    else:
                        print(" - ", end='')
                elif self.degrees[d] > 0 and not is_start:
                    print(" + ", end='')
                non_zero = True
                is_start = False
                print("{} * X^{}".format(self.abs(self.degrees[d]), d), end='')
        if non_zero == False:
            print('0', end='')
        print(" = 0")

    def polynomial_degree(self):
        degrees = sorted(self.degrees)
        d = 0
        if len(degrees):
            d = degrees[-1]
        print("Polynomial degree:", d)