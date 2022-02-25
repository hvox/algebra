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

    def det(self):
        if self.size[0] != self.size[1]:
            return 0
        raise NotImplemented()

    def interactive_determinant(self):
        if self.size[0] != self.size[1]:
            yield "Determinant is not defined for non-square matrix."
            return
        rows = list(self.values)
        multiplier = Rational(1)
        for i in range(self.size[0]):
            for j in range(i, self.size[0]):
                if rows[j][i] != 0:
                    if i != j:
                        yield f"Let's switch the row {i+1} and {j+1}."
                        rows[i], rows[j] = rows[j], rows[i]
                        multiplier *= -1
                        yield Matrix(*rows)
                    break
            else:
                yield "Now, tt is easy to see that the determinant is zero."
                yield 0
                return
            for j in range(i + 1, self.size[0]):
                if rows[j][i] == 0:
                    continue
                ratio = - rows[j][i] / rows[i][i]
                yield f"Add the multiple of {ratio} of the row {i + 1} to the row {j + 1}."
                rows[j] = tuple(x + ratio * y for x, y in zip(rows[j], rows[i]))
                yield Matrix(*rows)
        yield "Now we can find the determinant by multiplying all the diagonal elements of the matrix."
        equation = ""
        if multiplier != Rational(1):
            equation = str(multiplier)
        for i in range(self.size[0]):
            multiplier *= rows[i][i]
            if equation:
                equation += " * "
            equation += str(rows[i][i])
        yield f"{equation} = {multiplier}"
        yield multiplier
        return
