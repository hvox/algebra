#!/usr/bin/env python3
"""
Display results of different operations on two numbers.

Usage: {script} [options] [--] X Y

Options:
   -h, --help   Show this screen and exit.
   --verbose    Raise verbosity level.

Arguments:
    X           Operand #1.
    Y           Operand #2.
"""
import sys
from pathlib import Path
from typing import Any, Callable
from fractions import Fraction
from operator import add, mul, sub, floordiv
import math

debug: Callable[..., None]
noop: Any = lambda *args, **kwargs: None


def gcd(x: Fraction, y: Fraction):
    numerator = math.gcd(x.numerator, y.numerator)
    denominator = math.lcm(x.denominator, y.denominator)
    return Fraction(numerator, denominator)


OPERATIONS = {
    "x + y": add,
    "x - y": sub,
    "x × y": mul,
    "x / y": floordiv,
    "x % y": lambda x, y: x % abs(y),
    "GCD(x, y)": gcd,
    "LCM(x, y)": lambda x, y: x * y / gcd(x, y),
}


def main(script_name: str, *script_args: str):
    global debug
    doc = __doc__.format(script=Path(script_name).name)
    args = __import__("docopt").docopt(doc, script_args)
    debug = print if args["--verbose"] else noop
    debug(f"Running with arguments {dict(args)!r}")
    x, y = map(Fraction, (args["X"], args["Y"]))
    for op_name, op in OPERATIONS.items():
        print(op_name.replace("x", str(x)).replace("y", str(y)), "=", op(x, y))


if __name__ == "__main__":
    main(*sys.argv)
