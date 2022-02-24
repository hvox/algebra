from numbersretthinked import Rational


class Vector:
    def __init__(self, *xs):
        self.xs = tuple(map(Rational, xs))

    def __repr__(self):
        return f"Vector{self.xs}"

    def __str__(self):
        return "(" + ", ".join(map(str, self.xs)) + ")"

    def __iter__(self):
        yield from self.xs

    def __add__(u, v):
        return Vector(*(u + v for u, v in zip(u, v)))

    def __sub__(u, v):
        return Vector(*(u - v for u, v in zip(u, v)))
