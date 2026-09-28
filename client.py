"""KZG Polynomial Commitment Simulator Engine.
100% Python Standard Library.
"""

class KZGCommitment:
    """KZG polynomial commitment simulator over prime field."""
    P = 2147483647
    G = 7

    def __init__(self, s=5, degree=4):
        self.s = s
        self.srs = [pow(self.G, pow(s, i), self.P) for i in range(degree + 1)]

    def commit(self, poly_coeffs):
        c = 1
        for i, coeff in enumerate(poly_coeffs):
            c = (c * pow(self.srs[i], coeff, self.P)) % self.P
        return c

    def evaluate(self, poly_coeffs, z):
        res = 0
        for i, coeff in enumerate(poly_coeffs):
            res = (res + coeff * pow(z, i, self.P)) % self.P
        return res
