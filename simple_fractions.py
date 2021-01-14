from copy import copy
from math import gcd


def reduce(a: int, b: int):
    k = gcd(a, b)
    return a // k, b // k


class Fr:
    def __init__(self, fraction: str):
        num = fraction.split('/')
        self.numerator, self.denominator = reduce(int(num[0]), int(num[1]))

    def __add__(self, other):
        num_a = self.numerator
        num_b = other.numerator
        den_a = self.denominator
        den_b = other.denominator
        num_c = num_a * den_b + num_b * den_a
        den_c = den_a * den_b
        return reduce(num_c, den_c)

    def __sub__(self, other):
        other = copy(other)
        other.numerator *= -1
        return self.__add__(other)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    def __mul__(self, other):
        num = self.numerator * other.numerator
        den = self.denominator * other.denominator
        return reduce(num, den)

    def __truediv__(self, other):
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        return reduce(num, den)
