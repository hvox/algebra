BYCHKOVSKIY_NUMBER = 2**3**4


def bychkovskiy_number(x, k):
    assert isinstance(k, int), "k must be integer!"
    result = 1
    for k in range(k, 0, 2 * (k < 0) - 1):
        result = (x + k) ** result
    return x**result


if __name__ == "__main__":
    x = 2
    for n in range(-2, 10):
        print(f"{x}_{n} ->", bychkovskiy_number(x, n))
