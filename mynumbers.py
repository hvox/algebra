from fractions import Fraction


def ilog(n, base):
    log = 0
    while n % base == 0:
        n //= base
        log += 1
    return log


def fraction_to_recurring_decimal(fraction, max_digits=None):
    numerator, denominator = fraction.numerator, fraction.denominator
    integer_part = str(numerator // denominator)
    numerator = numerator % denominator
    digits, states = [], {}
    while numerator and numerator not in states:
        states[numerator] = len(digits)
        digits.append(numerator * 10 // denominator)
        numerator = numerator * 10 % denominator
        if max_digits is not None and len(digits) > max_digits:
            return None
    if not numerator:
        return integer_part + ("." + "".join(map(str, digits))) * bool(digits)
        if digits:
            return integer_part + "." + "".join(map(str, digits))
        return integer_part
    main_part = "".join(map(str, digits[: states[numerator]]))
    repeating_part = "(" + "".join(map(str, digits[states[numerator] :])) + ")"
    return integer_part + "." + main_part + repeating_part


def fraction_to_sum(fraction):
    numerator, denominator = fraction.numerator, fraction.denominator
    integer_part = numerator // denominator
    fractional_part = Fraction(numerator % denominator, denominator)
    if not fractional_part:
        return f"{integer_part}"
    return f"{integer_part}+" * bool(integer_part) + f"{fractional_part}"


def fraction_to_short_str(fraction):
    sum_representation = fraction_to_sum(fraction)
    decimal = fraction_to_recurring_decimal(fraction, len(sum_representation))
    if decimal is None or len(sum_representation) < len(decimal):
        return sum_representation
    return decimal


class Rational(Fraction):
    def as_recurring_decimal(self):
        return fraction_to_recurring_decimal(self)

    def as_sum(self):
        return fraction_to_sum(self)

    def as_fraction(self):
        return str(Fraction(self))

    def as_short_string(self):
        return fraction_to_short_str(self)

    def __str__(self):
        return self.as_short_string()

    def to_tex(self):
        fraction = str(Fraction(self))
        if "/" not in fraction:
            return fraction
        return "\\frac{" + fraction.replace("/", "}{") + "}"

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
