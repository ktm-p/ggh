import numpy as np
import random
import Utils

random.seed(69)

class GGH:
    def __init__(self, dimension:int=2, sigma:int=3, thresh:int=1000):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = self.generate_private_key()
        self.unimodular = self.generate_unimodular(100).astype(int)

        self.public_key = self.unimodular @ self.private_key

    def hadamard_ratio(self, matrix:np.array) -> float:
        _, log_determinant = np.linalg.slogdet(matrix)
        determinant = np.exp(log_determinant)
        norms = np.prod(np.linalg.norm(matrix, ord=2, axis=1))
        ratio = (determinant / norms)**(1 / self.dimension)

        print("Determinant:", determinant)
        print("Norms:", norms)
        return ratio

    def check_basis(self, matrix:np.array) -> bool:
        return np.linalg.matrix_rank(matrix) == self.dimension

    def generate_private_key(self) -> np.array:
        basis = None
        while True:
            vecs = []
            for i in range(self.dimension):
                vec = []
                for j in range(self.dimension):
                    vec.append(random.randint(-self.thresh, self.thresh))
                vecs.append(vec)
            
            basis = np.array(vecs)
            if self.check_basis(basis):
                print("break")
                break
            
        print("Basis:", basis)
        print("Hadamard Ratio:", self.hadamard_ratio(basis))
        return basis

    def check_unimodular(self, matrix:np.array) -> bool:
        determinant = round(np.linalg.det(matrix))
        print("Matrix:", matrix)
        print("Determinant:", determinant)
        if not (determinant == 1 or determinant == -1):
            print("Not Unimodular")
            return False
        else:
            print("Unimodular")
            return True

    def generate_unimodular(self, iters:int=-1) -> np.array:
        identity = np.eye(self.dimension, dtype=int)
        if iters == -1:
            iters = self.dimension**2

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

        return identity

inst = GGH(dimension=3)
inst.check_unimodular(inst.unimodular)