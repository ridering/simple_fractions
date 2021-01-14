from math import gcd


def reduce(a, b):
    k = gcd(a, b)
    return a // k, b // k


class Fr:
    def __init__(self, fraction: str):
        num = fraction.split('/')
        self.numerator, self.denominator = reduce(int(num[0]), int(num[1]))
