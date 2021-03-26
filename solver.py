# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    solver.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/24 18:39:56 by aihya             #+#    #+#              #
#    Updated: 2021/03/26 18:53:08 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math

class Solver:

    def __init__(self, terms):
        # print(terms)
        self.terms = terms
        
        self.highest_degr = sorted(terms.keys())[-1]

    def abs(self, num):
        return num if num >= 0 else -num

    def sqrt(self, num, eps=0.0000001):
        Xn = num
        Xnp1 = 0.5 * (Xn + (num / Xn))
        
        while abs(Xnp1 - Xn) >= eps:
            Xn = Xnp1
            Xnp1 = 0.5 * (Xn + (num / Xn))
        
        return Xn
        

    def discriminant(self):
        # B^2 - 4*A*C

        a = 0
        if self.terms.get(2):
            a = self.terms.get(2)['fact']
        b = 0
        if self.terms.get(1):
            b = self.terms.get(1)['fact']
        c = 0
        if self.terms.get(0):
            c = self.terms.get(0)['fact']

        return (b ** 2) - (4 * a * c), a, b, c

    def solve_quadratic(self):
        delta, a, b, c = self.discriminant()

        if delta < 0:
            print('Discriminant is strictly Negative.')
            print('No solutions in IR.')
            exit(0)
        if delta == 0:
            x = -b / (2 * a)
            if x == 0:
                x = int(x)
            print('Solution:', x)
        if delta > 0:
            print('Discriminant is strictly Positive.')
            x1 = (-b + self.sqrt(delta)) / (2 * a)
            x2 = (-b - self.sqrt(delta)) / (2 * a)
            print('X1 = {}\nX2 = {}'.format(x1, x2))

    def solve_linear(self):
        pass

    def solve_constant(self):
        pass

    def solve(self):
        # Polynomial degree
        print('Polynomial degree:', self.highest_degr)

        if self.highest_degr > 2:
            print('Error: Cannot solve this equation, degree greater than 2.')
            if sorted(self.terms.keys())[0] < 0:
                print('Error: Equation contains negative exponents')
            exit(1)
        if sorted(self.terms.keys())[0] < 0:
            print('Error: Equation contains negative exponents')
            exit(1)

        if self.highest_degr == 2:
            self.solve_quadratic()
        elif self.highest_degr == 1:
            self.solve_linear()
        else:
            self.solve_constant()
