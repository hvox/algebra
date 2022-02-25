from numbersretthinked import Rational
from human_api import Message, raise_messages
import scipy.linalg as linalg
import matrices


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


def are_linearly_independent(vectors):
    for i, v in enumerate(vectors):
        if all(x == 0 for x in v):
            yield "Vector {i + 1} is a zero vector. So the whole system is linearly dependent."
            yield False
    if len(vectors) < 2:
        yield "There are not enough vectors to be linearly dependent."
        yield True
        return
    yield "Let's build matrix out of these vectors."
    m = matrices.Matrix(*vectors)
    yield m
    yield "Let's find determinant of the matrix."
    determinant = [None]
    yield from raise_messages(m.interactive_determinant(), determinant)
    if determinant[0] == 0:
        yield "The determinant is zero, so the vectors are linearly dependent."
        yield False
        return
    yield "The determinant does not equals to zero, so the vectors are linearly independent."
    yield True
    return


def try_to_demonstrate_linear_dependence(vectors):
    for i, v in enumerate(vectors):
        if all(x == 0 for x in v):
            yield "Vector {i + 1} is a zero vector. So the whole system is linearly dependent."
            coeffs = [0] * len(vectors)
            coeffs[i] = 1
            yield coeffs
    if len(vectors) < 2:
        yield "There are not enough vectors to be linearly dependent."
        yield False
        return
    yield "Let's build matrix out of these vectors."
    m = matrices.Matrix(*vectors)
    yield m
    yield "Let's transform the matrix to triangle form."
    triangle = [None]
    yield from raise_messages(m.to_triangle(), triangle)
    m = triangle[0]
    d = m.det()
    if det != 0:
        yield "The matrix determinant does not equals to zero, so the vectors are linearly independent."
        yield False
        return
    determinant = [None]
    yield from raise_messages(m.interactive_determinant(), determinant)
    if determinant[0] == 0:
        yield "The determinant is zero, so the vectors are linearly dependent."
        yield False
        return
    linalg
    # TODO sovle system of equations
    raise NotImplemented()
    yield "The determinant does not equals to zero, so the vectors are linearly independent."
    yield True
    return
