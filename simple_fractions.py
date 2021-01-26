from copy import copy
from math import gcd
from typing import Tuple, overload, List


class Fr:
    numerator: int
    denominator: int
    __nested_fractions: List

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, fraction: str) -> None:
        ...

    @overload
    def __init__(self, fraction: Tuple[int, int]) -> None:
        ...

    @overload
    def __init__(self, numerator: int, denominator: int) -> None:
        ...

    def __init__(self, *args):
        self.__nested_fractions = ['']
        if len(args) == 0:
            self.numerator = 0
            self.denominator = 1
        elif len(args) == 1:
            num = args[0]
            if type(num) == str:
                fraction = self.__parse_string(num)
                self.numerator = fraction.numerator
                self.denominator = fraction.denominator
            elif type(num) == tuple:
                self.numerator, self.denominator = self.__reduce(*num)
            elif type(num) == Fr:
                self.numerator = num.numerator
                self.denominator = num.denominator
        elif len(args) == 2:
            self.numerator, self.denominator = self.__reduce(*args)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    @staticmethod
    def __count(command, a, b):
        commands = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a / b
        }
        return commands[command]

    @staticmethod
    def __reduce(a: int, b: int):
        k = gcd(a, b)
        if b < 0:
            b *= -1
            a *= -1
        return a // k, b // k

    @staticmethod
    def __check_fr(obj):
        if type(obj) != Fr:
            obj = Fr(obj)
        return obj

    def __parse_string(self, num):
        last_char = ''
        operators = {
            '(': lambda: self.__nested_fractions.append(''),
            '+': lambda: self.__make_fraction('+'),
            '*': lambda: self.__make_fraction('*'),
            '-': lambda: self.__add_part('-') if last_char in '*/-+(' else self.__make_fraction('-'),
            '/': lambda: self.__make_fraction('/') if last_char == ')' else self.__add_part('/'),
            ' ': lambda: ...,
            ')': lambda: self.__closing_bracket_func()
        }
        for char in num:
            if func := operators.get(char):
                func()
            else:
                self.__nested_fractions[-1] += char
            if char != ' ':
                last_char = char
        self.__compress_part()
        return self.__nested_fractions[0]

    def __add_part(self, char):
        self.__nested_fractions[-1] += char

    def __find_last_bracket(self):
        for i, item in enumerate(reversed(self.__nested_fractions)):
            if type(item) != Fr and item == '':
                return len(self.__nested_fractions) - i - 1
        return -1

    def __closing_bracket_func(self):
        ind = self.__find_last_bracket() + 1
        self.__compress_part(ind)
        self.__nested_fractions[-1] = self.__nested_fractions.pop()

    def __compress_part(self, ind=0):
        self.__make_fraction()
        while len(self.__nested_fractions[ind:]) > 1:
            exp = self.__find_priority(ind) + ind
            command = self.__nested_fractions.pop(exp)
            b = self.__nested_fractions.pop(exp)
            self.__nested_fractions[exp - 1] = self.__count(command, self.__nested_fractions[exp - 1], b)

    def __find_priority(self, ind=0):
        mul_div = -1
        add_sub = -1
        for i, item in enumerate(self.__nested_fractions[ind:]):
            if type(item) != Fr:
                if item in '*/':
                    mul_div = i
                    break
                elif item in '+-':
                    add_sub = i
        if mul_div != -1:
            return mul_div
        return add_sub

    def __make_fraction(self, char=None):
        if type(self.__nested_fractions[-1]) != Fr:
            num = self.__nested_fractions[-1].split('/')
            if len(num) == 1:
                self.__nested_fractions[-1] = Fr(int(num[0]), 1)
            else:
                self.__nested_fractions[-1] = Fr(int(num[0]), int(num[1]))
        if char:
            self.__nested_fractions.extend((char, ''))

    def __add__(self, other):
        other = self.__check_fr(other)
        num_a = self.numerator
        num_b = other.numerator
        den_a = self.denominator
        den_b = other.denominator
        num_c = num_a * den_b + num_b * den_a
        den_c = den_a * den_b
        return Fr(num_c, den_c)

    def __sub__(self, other):
        other = copy(self.__check_fr(other))
        other.numerator *= -1
        return self.__add__(other)

    def __mul__(self, other):
        other = self.__check_fr(other)
        num = self.numerator * other.numerator
        den = self.denominator * other.denominator
        return Fr(num, den)

    def __truediv__(self, other):
        other = self.__check_fr(other)
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        return Fr(num, den)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rdiv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return Fr(-self.numerator, self.denominator)

    def __pos__(self):
        return Fr(self.numerator, self.denominator)

    def __invert__(self):
        return Fr(self.denominator, self.numerator)

    def __eq__(self, other):
        other = self.__check_fr(other)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        other = self.__check_fr(other)
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __gt__(self, other):
        other = self.__check_fr(other)
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __bool__(self):
        return self.numerator != 0
