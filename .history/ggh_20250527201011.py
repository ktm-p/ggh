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

    def generate_unimodular(self):
        print(self.dimension)