from numbersretthinked import Rational


class Matrix:
    def __init__(self, *values):
        #print("mat", values)
        self.values = tuple(map(lambda row: tuple(map(Rational, row)), values))
        self.size = (len(values), len(values[0]))

    def __repr__(self):
        return f"Matrix{self.values}"

    def __str__(self):
        rows = ["\t" + "\t".join(map(str, row)) for row in self.values]
        return "\n".join(rows)

    def __iter__(self):
        for row in self.values:
            yield from row

    def __add__(u, v):
        result_rows = []
        for r1, r2 in zip(u.values, v.values):
            result_rows.append(tuple(x + y for x, y in zip(r1, r2)))
        return Matrix(*result_rows)

    def __sub__(u, v):
        result_rows = []
        for r1, r2 in zip(u.values, v.values):
            result_rows.append(tuple(x - y for x, y in zip(r1, r2)))
        return Matrix(*result_rows)
