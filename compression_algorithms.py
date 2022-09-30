from fractions import Fraction
from math import log, ceil


def fraction_to_bin(number, digits: int) -> str:
    number, representation = Fraction(number), []
    for _ in range(digits):
        number *= 2
        representation.append("01"[number >= 1])
        number %= 1
    return representation


def shannon(frequencies: list[int], n: int = 2) -> list[tuple[int, ...]]:
    assert n == 2
    frequencies = list(map(Fraction, reversed(sorted(frequencies))))
    whole, encoding, left = sum(frequencies), [], 0
    for freq in frequencies:
        digits = ceil(-log(freq / whole, 2))
        encoding.append(fraction_to_bin(left / whole, digits))
        left += freq
    return encoding


def _shannon_fano(frequencies: list[int], n: int = 2):
    if len(frequencies) <= n:
        if len(frequencies) < 2:
            yield ()
            return
        yield from ((i,) for i, _ in enumerate(frequencies))
        return
    separators = [0]
    whole, left, i = sum(frequencies), 0, 0
    for separator in range(1, n):
        separator = whole / n * separator
        while abs(left + frequencies[i] - separator) < abs(left - separator):
            left += frequencies[i]
            i += 1
        separators.append(i)
    separators.append(len(frequencies))
    for part in range(n):
        i, j = separators[part], separators[part + 1]
        for tail in _shannon_fano(frequencies[i:j], n):
            yield (part,) + tail


def shannon_fano(frequencies: list[int], n: int = 2) -> list[tuple[int, ...]]:
    sorted_freqs = list(sorted(enumerate(frequencies), key=lambda x: -x[1]))
    encoding = [None] * len(sorted_freqs)
    for i, code in enumerate(_shannon_fano([f for _, f in sorted_freqs], n)):
        encoding[sorted_freqs[i][0]] = code
    return encoding


probs = [0.36, 0.18, 0.18, 0.12, 0.09, 0.07]
print(probs)
print("Shannon: ", ["".join(map(str, t)) for t in shannon(probs)])
print("Shannon-Fano: ", ["".join(map(str, t)) for t in shannon_fano(probs)])
