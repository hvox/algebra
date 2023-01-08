from fractions import Fraction as Rat
from math import log, ceil
from queue import PriorityQueue

Encoding = list[tuple[int, ...]]


def fraction_to_bin(number, digits: int) -> str:
    number, representation = Rat(number), []
    for _ in range(digits):
        number *= 2
        representation.append("01"[number >= 1])
        number %= 1
    return "".join(representation)


def int_to_digits(number: int, base: int = 2) -> tuple[int, ...]:
    digits = [number % base]
    number //= base
    while number:
        digits.append(number % base)
        number //= base
    return tuple(digits)


def same_length(frequencies: list[Rat], n: int = 2) -> Encoding:
    digits = 1
    while n ** digits < len(frequencies):
        digits += 1
    encoding = [int_to_digits(i, n) for i in range(len(frequencies))]
    for i, code in enumerate(encoding):
        encoding[i] = code + (0,) * (digits - len(code))
    return encoding


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


def huffman(frequencies: list[Rat], n: int = 2) -> Encoding:
    assert n == 2
    queue = PriorityQueue()
    for i, freq in enumerate(frequencies):
        queue.put((freq, [((), i)]))
    for _ in range(len(frequencies) - 1):
        f2, right = queue.get()
        f1, left = queue.get()
        result = [((0,) + code, i) for code, i in left]
        result += [((1,) + code, i) for code, i in right]
        queue.put((f1 + f2, result))
    encoding = [()] * len(frequencies)
    for code, i in queue.get()[1]:
        encoding[i] = code
    return encoding


# TODO: add checker if coding is decodable


probs = [Rat(x) for x in "0.36 0.18 0.18 0.12 0.09 0.07".split()]
print(" ".join(map(str, map(float, probs))))
for name, f in (
    ("Same length", same_length),
    ("Shannon", shannon),
    ("Shannon(shrinked)", shannon_shrinked),
    ("Shannon-Fano", shannon_fano),
    ("Huffman", huffman),
):
    encoding = f(probs)
    avg_len = sum(len(code) * p for code, p in zip(encoding, probs))
    print(f"{name:18} avg_len =", float(avg_len))
    print(" ", " ".join("".join(map(str, x)) for x in encoding))
