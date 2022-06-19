import math

from frozendict import frozendict

from mynumbers import Rational


def normalize_root(x):
    if isinstance(x, (set, frozenset)):
        return frozenset(x)
    if isinstance(x, tuple) and x[0] == "+√":
        return frozenset({x})
    factors, r = [], x
    for p in range(2, math.isqrt(x)):
        if x % p == 0:
            x //= p
            factors.append(p)
            if x % p == 0:
                raise ValueError(f"{x} has factor {p}^2")
    if x != 1:
        factors.append(x)
    return frozenset(factors)


def root_to_str(roots):
    result, number = [], 1
    for root in roots:
        match root:
            case int(x):
                number *= x
            case "+√", int(x):
                result.append(f"√({x}+√{x})")
    if number != 1:
        result.append(f"√{number}")
    return "".join(result) if result else ""


class LCoQI:
    def __init__(self, coeffs):
        coeffs = {frozenset(normalize_root(r)): c for r, c in coeffs.items()}
        self.coeffs = frozendict(coeffs)

    def __str__(self):
        terms = []
        for root, coef in self.coeffs.items():
            root = root_to_str(root)
            terms.append(str(coef) + root if coef != 1 else root or "1")
        return " + ".join(terms) if terms else "0"

    def __repr__(self):
        return __class__.__name__ + f"({self.coeffs})"

    def __add__(self, other):
        result = dict(self.coeffs)
        for root, coef in other.coeffs.items():
            result[root] = result.get(root, 0) + coef
        return LCoQI({root: coef for root, coef in result.items() if coef})

    def __sub__(self, other):
        result = dict(self.coeffs)
        for root, coef in other.coeffs.items():
            result[root] = result.get(root, 0) - coef
        return LCoQI({root: coef for root, coef in result.items() if coef})

    def __mul__(self, other):
        if not len(self.coeffs) == len(other.coeffs) == 1:
            result = LCoQI({})
            for root1, coef1 in self.coeffs.items():
                for root2, coef2 in other.coeffs.items():
                    result += LCoQI({root1: coef1}) * LCoQI({root2: coef2})
            return result
        root1, coef1 = next(iter(self.coeffs.items()))
        root2, coef2 = next(iter(other.coeffs.items()))
        additional_factors = []
        coef, root = coef1 * coef2, root1.symmetric_difference(root2)
        for r in root1.intersection(root2):
            match r:
                case int(natural):
                    coef *= natural
                case "+√", int(x):
                    additional_factors.append(LCoQI({1: x, x: 1}))
        result = LCoQI({root: coef})
        for factor in additional_factors:
            result *= factor
        return result

    def __pow__(self, power: int):
        n = abs(power)
        result, factor = LCoQI({1: 1}), self
        while n:
            if n % 2 == 1:
                result *= factor
            n //= 2
            factor *= factor
        return result if power >= 0 else result.inverse()


if __name__ == "__main__":
    x = LCoQI({("+√", 2): 1})
    print(f"x = {x}")
    for n in range(0, 32):
        print(f"x^{n} = {x**n}")
