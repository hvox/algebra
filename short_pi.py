from time import time
from itertools import count

__import__("sys").set_int_max_str_digits(2**31 - 1)


# Based on Newton / Euler Convergence Transformation:
# https://en.wikipedia.org/wiki/Approximations_of_%CF%80#cite_ref-67

digits = 10000
start = time()
n = 10 ** (digits + 10)
pi = m = 2 * n
for i in count(1):
    pi += (m := m * i // (2 * i + 1))
    if not m:
        break
pi = str(pi)[: digits + 1]
print(pi[:30] + "..." + pi[-30:])
print("digits:", digits, " time:", time() - start)
