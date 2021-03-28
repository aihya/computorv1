# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aihya <aihya@student.1337.ma>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:15:14 by aihya             #+#    #+#              #
#    Updated: 2021/03/28 18:04:25 by aihya            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
class Parser:

    def __init__(self, exp):
        self.sides = exp.split('=', 1)
        self.l_terms = None
        self.r_terms = None
        self.err = False
        self.errmsgs = []
        self.terms = []

    def extract_terms(self, string):
        num_grp = r"([+-]\s*|)\d+(\.\d+|)"
        afx_grp = r"(\s*\^\s*({})|)".format(num_grp)
        bfx_grp = r"(\s*{}\s*\*?\s*|\s*[+-]\s*|)".format(num_grp)
        pattern = r"(\s*{}[Xx]{}\s*|\s*{}\s*)".format(bfx_grp,
                                                   afx_grp, num_grp)
        m = re.findall(pattern, string)
        matches = [tup[0] for tup in m]
        return matches

    def term_obj(self, term=None, sign=None, fact=None, degr=None, X=None):
        return {
            'term': term,
            'sign': sign,
            'fact': fact,
            'degr': degr,
            'X': X
        }

    def is_empty(self, string):
        _is_empty = True
        for c in string:
            if c == ' ':
                continue
            _is_empty = False
            break
        return _is_empty

    def format_err(self, terms, side):
        res = ''

        if terms:
            for i, term in enumerate(terms):
                splitted = side.split(term, 1)
                if splitted[0]:
                    res += '\x1b[1;4;31m{}\x1b[0m'.format(splitted[0])
                    self.err = True
                if i != 0 and not self.is_sign_preceded(i, term):
                    res += '\x1b[1;4;31m{}\x1b[0m'.format(term)
                    self.err = True
                else:
                    res += '\x1b[32m{}\x1b[0m'.format(term)
                side = splitted[-1]
            if splitted[-1]:
                res += '\x1b[1;4;31m{}\x1b[0m'.format(splitted[-1])
                self.err = True
        else:
            res += '\x1b[1;4;31m{}\x1b[0m'.format(side)
            self.err = True
        return res

    def show_exp(self):
        res = ''

        if len(self.sides) == 2:
            lres = self.format_err(self.l_terms, self.sides[0])
            rres = self.format_err(self.r_terms, self.sides[1])
            res = '{}\x1b[32m=\x1b[0m{}'.format(lres, rres)
        elif len(self.sides) == 1:
            lres = self.format_err(self.l_terms, self.sides[0])
            res = '{}\x1b[32m\x1b[0m'.format(lres)
        print('Expression: "{}"'.format(res))

    # Terms parsing functions ##################################################

    def abs(self, num):
        return num if num >= 0 else -1 * num

    def conv_num(self, num):
        return float(num) if '.' in num else int(num)

    def is_sign_preceded(self, i, term):
        sign_match = re.match(r'^\s*[+-]', term)
        if i != 0 and sign_match == None:
            return False
        return True

    def nospace(self, string):
        return string.replace(' ', '')

    def parse_term(self, term, side):
        # Parse each term individually

        t = self.term_obj()
        t['term'] = term
        if 'X' in term or 'x' in term:

            bfx = re.search(r'^\s*(([+-]\s*|)\d+(\.\d+|))', term)
            if bfx:
                # print(bfx.groups())
                bfx = self.nospace(bfx.groups()[0])

            afx = re.search(r'\^\s*(([+-]\s*|)\d+(\.\d+|))', term)
            if afx:
                # print(afx.groups())
                afx = self.nospace(afx.groups()[0])

            t['fact'] = self.conv_num(bfx) if bfx else None
            t['degr'] = self.conv_num(afx) if afx else None
            t['X'] = True
        else:
            t['fact'] = self.conv_num(self.nospace(term))
        
        sign = re.search(r'^\s*([+-])', term)
        
        if sign:
            _ = sign.groups()[0]
            t['sign'] = -1 if _ == '-' else 1
        else:
            t['sign'] = 1

        t['sign'] *= side
        if t['fact']:
            t['fact'] *= side

        # print(term, t)
        return t
    ############################################################################

    def reduce_terms(self):
        # self.terms will be replaced with dictionary containing all terms
        # in a reduced format

        terms = dict()

        def adjust_term(degr, term):

            term.pop('term')

            if term['fact'] == None:
                term['fact'] = term['sign']

            if term['X'] == True and term['degr'] == None:
                term['degr'] = 1

            if term['X'] == None:
                term['degr'] = 0

            # print('->', term)
            if degr not in terms.keys():

                # Add term to dictionary if it does not already exist
                terms[degr] = term
                if terms[degr]['degr'] == None:
                    terms[degr]['degr'] = degr
                return

            # Adjust factor value
            terms[degr]['fact'] += term['fact']

            # Adjust the sign of the term
            terms[degr]['sign'] = 1 if terms[degr]['fact'] >= 0 else -1

        for term in self.terms:
            # 2 or 2 * X^0
            if term['X'] == None or (term['X'] and term['degr'] == 0):
                adjust_term(0, term)
            elif term['X'] and (term['degr'] == None or term['degr'] == 1):
                adjust_term(1, term)
            else:
                adjust_term(term['degr'], term)

        self.terms = terms

    def show_reduced_format(self):
        frmt = []
        # print(sorted(self.terms.keys()))
        for i, degr in enumerate(sorted(self.terms.keys())):
            fact = self.terms[degr]['fact']
            sign = self.terms[degr]['sign']

            # Show only the terms with non-null fact
            if fact != 0:
                t = ''
                if sign == -1:
                    t = '-' if i == 0 else '- '
                if sign == 1:
                    t = '' if i == 0 else '+ '
                if degr == 0:
                    t += str(self.abs(fact))
                    frmt.append(t)
                else:
                    if degr == 1:
                        if self.abs(fact) == 1:
                            t += 'X'
                        else:
                            t += '{} * X'.format(self.abs(fact))
                        frmt.append(t)
                    else:
                        if self.abs(fact) == 1:
                            t += 'X^{}'.format(str(degr))
                        else:
                            t += '{} * X^{}'.format(str(self.abs(fact)), str(degr))
                        frmt.append(t)

        print('Reduced form: {} = 0'.format(' '.join(frmt) if len(frmt) else 0))

    def filter_terms(self):
        filtered = dict()
        
        for degr in self.terms:
            if self.terms[degr]['fact'] != 0:
                filtered[degr] = self.terms[degr]
        if len(filtered) == 0:
            filtered[0] = self.term_obj(sign=1, fact=0, degr=0)
            filtered[0].pop('term')
        self.terms = filtered

    def parse(self):
        # Terms extraction.
        if len(self.sides) == 2:
            if self.is_empty(self.sides[0]):
                self.err = True
                self.errmsgs.append('Empty left side')
            else:
                self.l_terms = self.extract_terms(self.sides[0])
                # print(self.l_terms)
            if self.is_empty(self.sides[1]):
                self.err = True
                self.errmsgs.append('Empty right side')
            else:
                self.r_terms = self.extract_terms(self.sides[1])
                # print(self.r_terms)
        elif len(self.sides) == 1:
            if not self.is_empty(self.sides[0]):
                self.l_terms = self.extract_terms(self.sides[0])
                # self.r_terms = ['0']
            else:
                self.err = True
                self.errmsgs.append('Empty expression')
        # End

        # Show expression and error if there's any.
        self.show_exp()
        if self.err:
            for err in self.errmsgs:
                print('Error: {}'.format(err))
            return None
        # End

        # Parse left terms
        for t in self.l_terms:
            self.terms.append(self.parse_term(t, 1))
        # End

        non_zero = False
        for t in self.terms:
            if t['fact'] != 0:
                non_zero = True
                break
        
        # Parse right terms
        sign = -1 if non_zero else 1
        if self.r_terms:
            for t in self.r_terms:
                self.terms.append(self.parse_term(t, sign))

        # for t in self.r_terms:
        #     self.terms.append(self.parse_term(t, -1))
        # End


        self.reduce_terms()
        self.filter_terms()

        self.show_reduced_format()
        return self.terms


# parser = Parser(sys.argv[1])
# if parser == None:
#     exit(1)
# terms = parser.parse()
# if terms == None:
#     exit(1)
# print('Final parsing result:', terms)
