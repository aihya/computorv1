# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    solver.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/24 18:39:56 by aihya             #+#    #+#              #
#    Updated: 2021/04/01 13:50:57 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

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

        a = self.terms.get(2)['fact'] if self.terms.get(2) else 0
        b = self.terms.get(1)['fact'] if self.terms.get(1) else 0
        c = self.terms.get(0)['fact'] if self.terms.get(0) else 0

        return (b * b) - (4 * a * c), a, b, c

    def set_int(self, num):
        if float(num) != int(num):
            return num
        return int(num)

    def solve_quadratic(self):
        delta, a, b, c = self.discriminant()
        
        def non_null(coef):
            x1 = round((-b + self.sqrt(coef * delta)) / (2 * a), 6)
            x2 = round((-b - self.sqrt(coef * delta)) / (2 * a), 6)
            return x1 if x1 else 0, x2 if x2 else 0

        if delta < 0:
            print('Discriminant is strictly Negative.')

            rx1 = -b / (2 * a), 6
            ix1 = -self.sqrt(-delta) / (2 * a), 6
            s1 = '+' if ix1 >= 0 else ''

            rx2 = -b / (2 * a), 6
            ix2 = self.sqrt(-delta) / (2 * a), 6
            s2 = '+' if ix2 >= 0 else ''

            print('{:6f}{}{:6f}i\n{:6f}{}{:6f}i'.format(rx1, s1, ix1, rx2, s2, ix2))
        if delta == 0:
            print('Discriminant is Null')
            x = -b / (2 * a)
            if x == 0:
                x = int(x)
            print('Solution:', x)
        if delta > 0:
            print('Discriminant is strictly Positive.')
            
            x1 = round((-b - self.sqrt(delta)) / (2 * a), 6)
            x2 = round((-b + self.sqrt(delta)) / (2 * a), 6)

            print('{:6f}\n{:6f}'.format(x1, x2))

    def solve_linear(self):
        x = -self.terms[0]['fact'] if self.terms.get(0) else 0
        x = x / self.terms[1]['fact']
        print('Solution: {:6f}'.format(x))

    def solve_constant(self):
        if self.terms.get(0) and self.terms[0]['fact'] == 0:
            print('All real numbers are solutions.')
        else:
            print('Invalid expression')

    def solve(self):
        # Polynomial degree
        print('Polynomial degree:', self.highest_degr)

        if self.highest_degr > 2:
            print('Error: Equations with degrees higher than 2 are not supported.')
            if sorted(self.terms.keys())[0] < 0:
                print('Error: Equation contains negative exponents')
            return 1
        if sorted(self.terms.keys())[0] < 0:
            print('Error: Equation contains negative exponents')
            return 1

        if self.highest_degr == 2:
            self.solve_quadratic()
        elif self.highest_degr == 1:
            self.solve_linear()
        else:
            self.solve_constant()
