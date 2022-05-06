from fractions import Fraction


class Rational(Fraction):
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"


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
