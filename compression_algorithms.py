from fractions import Fraction as Rat
from math import log, ceil


def fraction_to_bin(number, digits: int) -> str:
    number, representation = Rat(number), []
    for _ in range(digits):
        number *= 2
        representation.append("01"[number >= 1])
        number %= 1
    return "".join(representation)


def shannon(frequencies: list[Rat], n: int = 2) -> list[tuple[int, ...]]:
    assert n == 2
    frequencies = [Rat(x) for x in reversed(sorted(frequencies))]
    whole, encoding, left = sum(frequencies), [], Rat(0)
    for freq in frequencies:
        digits = ceil(-log(freq / whole, 2))
        encoding.append(tuple(map(int, fraction_to_bin(left / whole, digits))))
        left += freq
    return encoding


def _shannon_fano(frequencies: list[Rat], n: int = 2):
    if len(frequencies) <= n:
        if len(frequencies) < 2:
            yield ()
            return
        yield from ((i,) for i, _ in enumerate(frequencies))
        return
    separators = [0]
    whole, left, i = sum(frequencies), Rat(0), 0
    for separator in range(1, n):
        sep = Rat(whole) / n * separator
        while abs(left + frequencies[i] - sep) < abs(left - sep):
            left += frequencies[i]
            i += 1
        separators.append(i)
    separators.append(len(frequencies))
    for part in range(n):
        i, j = separators[part], separators[part + 1]
        for tail in _shannon_fano(frequencies[i:j], n):
            yield (part,) + tail


def shannon_fano(frequencies: list[Rat], n: int = 2) -> list[tuple[int, ...]]:
    sorted_freqs = list(sorted(enumerate(frequencies), key=lambda x: -x[1]))
    encoding: list[tuple[int, ...]] = [()] * len(sorted_freqs)
    for i, code in enumerate(_shannon_fano([f for _, f in sorted_freqs], n)):
        encoding[sorted_freqs[i][0]] = code
    return encoding


probs = [0.36, 0.18, 0.18, 0.12, 0.09, 0.07]
print(probs)
print("Shannon: ", ["".join(map(str, t)) for t in shannon(probs)])
print("Shannon-Fano: ", ["".join(map(str, t)) for t in shannon_fano(probs)])
