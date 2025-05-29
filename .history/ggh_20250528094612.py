import numpy as np
import random
import Utils

random.seed(69)

class GGH:
    def __init__(self, dimension:int=2, sigma:int=3):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma

        self.private_key = ...
        self.unimodular = self.generate_unimodular()

        self.public_key = self.unimodular @ self.private_key

    def generate_unimodular(self, iters:int=-1):
        identity = np.eye(self.dimension, dtype=int)
        if iters == -1:
            iters = self.dimension // 2

        for i in range(200):
            operation = random.randint(0, 1)
            i = random.randint(0, self.dimension-1)
            j = random.randint(0, self.dimension-1)
            # Swap
            if operation == 0:
                identity[[i, j]] = identity[[j, i]]
            # Row Addition
            else:
                identity[i] += identity[j]

        return identity