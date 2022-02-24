from fractions import Fraction


class Rational(Fraction):
    def __str__(self):
        denominator = self.denominator
        denominator = f"/{denominator}" if denominator != 1 else ""
        return f"{self.numerator}{denominator}"
