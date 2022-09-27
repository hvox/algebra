from sympy import isprime as sympy_primality_test
import random
import time

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
JIM_SINCLAIR_BASES = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
MERSENNE_PRIME_EXPONENTS = (
    [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1_279, 2_203]
    + [2_281, 3_217, 4_253, 4_423, 9_689, 9_941, 11_213, 19_937, 21_701]
    + [23_209, 44_497, 86_243, 110_503, 132_049, 216_091, 756_839, 859_433]
    + [1_257_787, 1_398_269, 2_976_221, 3_021_377, 6_972_593, 13_466_917]
    + [20_996_011, 24_036_583, 25_964_951, 30_402_457, 32_582_657, 37_156_667]
    + [42_643_801, 43_112_609, 57_885_161, 74_207_281, 77_232_917, 82_589_933]
)


def mersene_prime(n):
    assert 0 < n <= 51
    return 2 ** MERSENNE_PRIME_EXPONENTS[n - 1] - 1


def lehmann(n):
    if n < 2:
        return False
    all_ones = True
    m = (n - 1) // 2
    for _ in range(50):
        a = random.randint(1, n - 1)
        a_to_the_m = pow(a, m, n)
        if a_to_the_m not in {1, n-1}:
            return False
        if a_to_the_m == n - 1:
            all_ones = False
    return not all_ones


def miller_rabin_copypasted_from_the_internet(n, k=10):
    if n < 5:
        return n in (2, 3)
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = random.randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


def fermat_primality_test(n):
    return n == 2 or n & 1 == 1 and pow(2, n - 1, n) == 1


def count_trailing_zeros(n):
    return (n & -n).bit_length() - 1


def miller_rabin(n):
    if n % 2 == 0 or n < 42:
        return n in SMALL_PRIMES
    s = count_trailing_zeros(n - 1)
    d = (n - 1) >> s
    for a in [SMALL_PRIMES, JIM_SINCLAIR_BASES][n.bit_length() > 64]:
        x = pow(a, d, n)
        if x != 1:
            for _ in range(s):
                if x == n - 1:
                    break
                x = pow(x, 2, n)
            else:
                return False
    return True


if __name__ == "__main__":
    primes = {x for x in range(2**16) if sympy_primality_test(x)}
    testers = [
        ("Fermat", fermat_primality_test),
        ("Miller-Rabin(stolen)", miller_rabin_copypasted_from_the_internet),
        ("Miller-Rabin", miller_rabin),
        ("sympy.isprime", sympy_primality_test),
        ("Lehmann", lehmann),
    ]
    t0 = time.time()
    for tester_name, test in testers:
        print(f" --- testing {tester_name}")
        for n in range(2**8):
            if (n in primes) != test(n):
                print(f"Wrong answer for {n}")
        print("Time of checking small numbers:", time.time() - t0)
        t0 = time.time()
        assert test(mersene_prime(21))
        print("Time of checking 21-st Mersenne prime:", time.time() - t0)
        t0 = time.time()
        assert not test(mersene_prime(20) - 12345)
        print("Time of checking some big composite number:", time.time() - t0)
        t0 = time.time()
        assert not test(mersene_prime(21) + 123456789)
        print("Time of checking bigger composite number:", time.time() - t0)
        t0 = time.time()
        assert not test(10**2000 + 4563)
        print(
            "Time of checking even bigger composite number:", time.time() - t0
        )
