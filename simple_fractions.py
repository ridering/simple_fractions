from copy import copy
from math import gcd
from typing import Tuple, overload


def reduce(a: int, b: int):
    k = gcd(a, b)
    return a // k, b // k


def check_fr(obj):
    if type(obj) in (str, tuple):
        obj = Fr(obj)
    return obj


class Fr:
    numerator: int
    denominator: int

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
        if len(args) == 0:
            self.numerator = 0
            self.denominator = 1
        elif len(args) == 1:
            num = args[0]
            if type(num) == str:
                num = num.split('/')
                self.numerator, self.denominator = reduce(int(num[0]), int(num[1]))
            elif type(num) == tuple:
                self.numerator, self.denominator = reduce(*num)
        elif len(args) == 2:
            self.numerator, self.denominator = reduce(*args)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    def __add__(self, other):
        other = check_fr(other)
        num_a = self.numerator
        num_b = other.numerator
        den_a = self.denominator
        den_b = other.denominator
        num_c = num_a * den_b + num_b * den_a
        den_c = den_a * den_b
        return Fr(num_c, den_c)

    def __sub__(self, other):
        other = copy(check_fr(other))
        other.numerator *= -1
        return self.__add__(other)

    def __mul__(self, other):
        other = check_fr(other)
        num = self.numerator * other.numerator
        den = self.denominator * other.denominator
        return Fr(num, den)

    def __truediv__(self, other):
        other = check_fr(other)
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
        other = check_fr(other)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        other = check_fr(other)
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __gt__(self, other):
        other = check_fr(other)
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __bool__(self):
        return self.numerator != 0
