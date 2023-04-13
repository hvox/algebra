from time import time
from math import isqrt, log2
from itertools import count
from pathlib import Path

PI_DIGITS = Path("./pi.txt").read_text().replace("\n", "")[2:]


def count_while(start, f):
    for i in count(start):
        if not f():
            break
        yield i


def compute_pi_digits(digits=64):
    # https://www.craig-wood.com/nick/articles/pi-chudnovsky/
    error_digits = 2 + round(log2(digits))
    a_sum = a = one = 10 ** (digits + error_digits)
    b_sum = 0
    for k in count_while(1, lambda: a):
        a = -24 * (6 * k - 5) * (2 * k - 1) * (6 * k - 1) * a // (k**3 * 640320**3)
        b_sum += a * k
        a_sum += a
    pi = 426880 * isqrt(10005 * one**2) * one
    pi //= 13591409 * a_sum + 545140134 * b_sum
    return pi // 10**error_digits


if __name__ == "__main__":
    print(compute_pi_digits(50))
    print("3" + PI_DIGITS[:50])
    for n in range(1, 6):
        digits = 10**n
        start = time()
        pi = compute_pi_digits(digits)
        dt = time() - start
        print(f"digits=10**{n} time={dt:0.5f}s {pi % 100:02}", PI_DIGITS[digits-2:digits])
        assert f"{pi % 100:02}" == PI_DIGITS[digits-2:digits]
