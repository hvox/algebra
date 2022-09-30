from fractions import Fraction as Rat
from math import log, ceil

Encoding = list[tuple[int, ...]]


def fraction_to_bin(number, digits: int) -> str:
    number, representation = Rat(number), []
    for _ in range(digits):
        number *= 2
        representation.append("01"[number >= 1])
        number %= 1
    return "".join(representation)


def shannon(frequencies: list[Rat], n: int = 2) -> Encoding:
    assert n == 2
    sorted_freqs = list(sorted(enumerate(frequencies), key=lambda x: -x[1]))
    frequencies = [freq for _, freq in sorted_freqs]
    whole, encoding, left = sum(frequencies), [], Rat(0)
    for freq in frequencies:
        digits = ceil(-log(freq / whole, 2))
        encoding.append(tuple(map(int, fraction_to_bin(left / whole, digits))))
        left += freq
    for i, code in enumerate(list(encoding)):
        encoding[sorted_freqs[i][0]] = code
    return encoding


def shrink_encoding(encoding: Encoding) -> Encoding:
    trie, paths = {}, []
    for code in encoding:
        node, path = trie, []
        for char in code:
            node.setdefault(char, [0, {}])[0] += 1
            path.append(node[char])
            node = node[char][1]
        paths.append(path)
    for i, code in enumerate(encoding):
        path = paths[i]
        while len(path) > 2 and path[~1][0] == 1:
            path.pop()
        encoding[i] = code[:len(path)]
    return encoding


def shannon_shrinked(frequencies: list[Rat], n: int = 2) -> Encoding:
    return shrink_encoding(shannon(frequencies, n))


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


def shannon_fano(frequencies: list[Rat], n: int = 2) -> Encoding:
    sorted_freqs = list(sorted(enumerate(frequencies), key=lambda x: -x[1]))
    encoding: Encoding = [()] * len(sorted_freqs)
    for i, code in enumerate(_shannon_fano([f for _, f in sorted_freqs], n)):
        encoding[sorted_freqs[i][0]] = code
    return encoding


probs = [Rat(x) for x in "0.36 0.18 0.18 0.12 0.09 0.07".split()]
print(" ".join(map(str, map(float, probs))))
for name, f in (
    ("Shannon", shannon),
    ("Shannon(shrinked)", shannon_shrinked),
    ("Shannon-Fano", shannon_fano),
):
    encoding = f(probs)
    avg_len = sum(len(code) * p for code, p in zip(encoding, probs))
    print(f"{name}: avg_len =", float(avg_len))
    print(" ", " ".join("".join(map(str, x)) for x in encoding))
