from mynumbers import GaloisField


def get_root(F, r):
    best_root = (0, 0)
    for n in range(1, F.size):
        good = set()
        for x in range(1, F.size):
            if (F(x) ** r) ** n == F(x):
                good.add(x)
        best_root = max(best_root, (len(good), n))
    return best_root


from math import isqrt
from sympy import primerange

for p in primerange(5, 2 ** 16):
    roots = []
    for root in range(2, 5):
        roots.append(get_root(GaloisField(p), root)[0] / (p - 1) * 100)
        roots[-1] *= 1 + ((root + 1) % 2)
    status = all(round(r) == 100 for r in roots)
    print(p, "->", " ".join(map(str, map(round, roots))), "<- COOL!" * status)
