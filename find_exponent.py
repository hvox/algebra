from mynumbers import GaloisField
from itertools import product
from sympy import primerange

def test_exponentness(f):
    p = len(f)
    points = 0
    for x, y in product(range(p//2), repeat=2):
        points += (f[x] * f[y]) % p == f[(x + y) % p]
    return points, set(f)


for p in primerange(5, 50):
    print(f"--- field of size {p} ---")
    for f in product(range(p), repeat=p):
        points, ys = test_exponentness(f)
        if len(ys) >= p//2 and points / p**2 >= 1/5: 
            print(f, round(100*len(ys)/p), round(100*points/p**2))
