import numpy as np
import random
from Utils.utils import Utils

random.seed(69)

class GGH:
    def __init__(self, dimension:int=2, sigma:int=3, thresh:int=1000):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = self.generate_private_key()
        self.unimodular = Utils.generate_unimodular(self.dimension)

        self.public_key = self.unimodular @ self.private_key

    def generate_private_key(self) -> np.array:
        basis = None
        while (not Utils.check_basis(self.dimension, basis)) or (Utils.hadamard_ratio(self.dimension, basis) < 0.7):
            vecs = []
            for _ in range(self.dimension):
                vec = []
                for _ in range(self.dimension):
                    vec.append(random.randint(-self.thresh, self.thresh))
                vecs.append(vec)
            
            basis = np.array(vecs)

        print("Basis:", basis)
        print("Hadamard Ratio:", Utils.hadamard_ratio(self.dimension, basis))
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

inst = GGH(dimension=3)
inst.check_unimodular(inst.unimodular)