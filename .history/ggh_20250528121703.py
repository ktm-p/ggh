import numpy as np
import random
import Utils

random.seed(69)

class GGH:
    def __init__(self, dimension:int=2, sigma:int=3):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma

        self.private_key = np.eye(self.dimension)
        self.unimodular = self.generate_unimodular(100).astype(int)

        self.public_key = self.unimodular @ self.private_key

    def generate_private_key(self):
        ...

    def generate_unimodular(self, iters:int=-1):
        identity = np.eye(self.dimension, dtype=int)
        if iters == -1:
            iters = self.dimension // 2

        for iter in range(iters):
            operation = random.randint(0, 2)

            # Picks indices to perform row operations on
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, self.dimension-1)
                j = random.randint(0, self.dimension-1)

            # Swap
            if operation == 0:
                identity[[i, j]] = identity[[j, i]]
            # Scaling
            elif operation == 1:
                multiplier = random.choice([-1, 1])
                identity[i] *= multiplier
            # Row Addition
            else:
                identity[i] += identity[j]

            identity = identity.astype(int)

            if not self.check_unimodular(identity):
                return identity

        return identity

    def check_unimodular(self, matrix:np.array):
        determinant = round(np.linalg.det(matrix))
        print("Matrix:", matrix)
        print("Determinant:", determinant)
        if not (determinant == 1 or determinant == -1):
            print("Not Unimodular")
            return False
        else:
            print("Unimodular")
            return True

inst = GGH()