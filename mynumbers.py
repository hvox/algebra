from fractions import Fraction


def ilog(n, base):
    log = 0
    while n % base == 0:
        n //= base
        log += 1
    return log


def fraction2str(numerator, denominator):
    integer_part = str(numerator // denominator)
    numerator = numerator % denominator
    digits, states = [], {}
    while numerator and numerator not in states:
        states[numerator] = len(digits)
        digits.append(numerator * 10 // denominator)
        numerator = numerator * 10 % denominator
    if not numerator:
        return integer_part + ("." + "".join(map(str, digits))) * bool(digits)
        if digits:
            return integer_part + "." + "".join(map(str, digits))
        return integer_part
    main_part = "".join(map(str, digits[: states[numerator]]))
    repeating_part = "(" + "".join(map(str, digits[states[numerator] :])) + ")"
    return integer_part + "." + main_part + repeating_part


class Rational(Fraction):
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"


class RecurringDecimal(Rational):
    def __str__(self):
        return fraction2str(self.numerator, self.denominator)


def GaloisField(p):
    class GaloisField:
        size = p

        def __init__(self, value):
            self.value = value % p

        def __repr__(self):
            return f"{__class__.__name__}({self.value})"

        def __str__(self):
            return str(self.value)

        def __add__(self, other):
            return self.__class__(self.value + getattr(other, "value", other))

        def __sub__(self, other):
            return self.__class__(self.value - getattr(other, "value", other))

        def __mul__(self, other):
            return self.__class__(self.value * getattr(other, "value", other))

        def __pow__(self, n):
            return self.__class__(pow(self.value, n, p))

        def __eq__(self, other):
            return self.value == getattr(other, "value", other)

    return GaloisField


def SignedGaloisField(p):
    class SignedGaloisField(GaloisField(p)):
        def __str__(self):
            if self.value * 2 > self.size:
                return str(-self.size + self.value)
            return str(self.value)

    return SignedGaloisField
