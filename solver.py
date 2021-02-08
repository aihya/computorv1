# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    solver.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/02 16:56:21 by aihya             #+#    #+#              #
#    Updated: 2021/02/08 16:30:35 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Solver:
    def __init__(self, terms):
        self.terms = terms
        self.degrees = dict()
        self.degree = 0
        self.reduce_eq()
        self.set_degree()
    
    def sqrt(self, num):
        thresh = 0.0000001

        x1 = num
        res = (x1 + (num / x1)) / 2
        while self.abs(x1 - res) >= thresh:
            x1 = res
            res = (x1 + (num / x1)) / 2
            
        return res

    def abs(self, n):
        if n < 0:
            return n * -1
        return n

    def reduce_eq(self):
        for term in self.terms:
            if term.degree in self.degrees:
                self.degrees[term.degree].set_factor(term.factor)
            else:
                self.degrees[term.degree] = term
    
    def set_degree(self):
        degrees = sorted(self.degrees)
        if len(degrees):
            self.degree = degrees[-1]

    def reduced_form(self):
        non_zero = False
        is_start = True

        sorted_degrees = sorted(self.degrees)
        print("Reduced form: ", end='')
        for d in sorted_degrees:
            if self.degrees[d].sign < 0:
                if is_start:
                    print("-", end='')
                else:
                    print(" - ", end='')
            elif self.degrees[d].sign > 0 and not is_start:
                print(" + ", end='')
            non_zero = True
            is_start = False
            print("{} * X^{}".format(self.abs(self.degrees[d].factor), d), end='')
        if non_zero == False:
            print('0', end='')
        print(" = 0")

    def polynomial_degree(self):
        print("Polynomial degree:", self.degree)

    def get_factor(self, d):
        return 0 if d not in self.degrees else self.degrees[d].factor

    def delta(self):
        # Delta = b^2 - 4*a*c
        a = self.get_factor(0)
        b = self.get_factor(1)
        c = self.get_factor(2)

        _delta = b*b - 4*a*c
        print(_delta)

        return a, b, _delta
    
    def solve_2(self):
        pass

    def solve_1(self):
        pass

    def solve_0(self):
        if 0 in self.degrees and self.degrees[0].factor != 0:
            print("¯\_(ツ)_/¯")
        else:
            print("Solution: All real numbers are solutions for this equation")

    def solutions(self):
        if self.degree == 0:
            self.solve_0()
        elif self.degree == 1:
            pass
        elif self.degree == 2:
            a, b, _delta = self.delta()
            if _delta == 0:
                x1 = -b / 2*a
                print(x1)
            elif _delta > 0:
                print("Disctiminant is strictly positive, the two solutions are:")
                x1 = (-b + self.sqrt(_delta)) - 2*a
                x2 = (-b - self.sqrt(_delta)) - 2*a
                print("{:.6f}\n{:.6f}".format(x1, x2))
            else:
                print("Discriminant is strictly negative, solutions are complexe.")
        else:
            print("I can't solve polynomials strictly greater then 2.")