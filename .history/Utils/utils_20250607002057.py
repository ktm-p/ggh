import numpy as np
import random
from flint import fmpz_mat, fmpz, fmpq, fmpq_mat
'''
    - encode(message): Takes in a string message and encodes it using UTF-8. Returns a list of integers.
    - decode(message): Takes in a list of integers. Decodes using UTF-8, returning a string.
    - babai_round(basis, vec): Takes in a (nearly-orthogonal) lattice basis and integer vector. Rounds the vector to the nearest lattice point.
    - generate_unimodular(dimension, iters): Given a dimension and iters operations, randomly apply operations to the nxn identity matrix to generate a unimodular matrix U.
    - hadamard_ratio(dimension, matrix): Given a matrix of a given dimension, calculate its Hadamard Ratio.
'''
class Utils:
    def encode(message: str) -> list[int]:
        encoded = message.encode("utf8")
        return np.array(list(encoded))

    def decode(message: list[int]) -> str:
        message_bytes = bytes(message)
        return message_bytes.decode("utf8")

    def babai_round(basis: np.array , vec: np.array) -> np.array:
        t = np.round(vec @ np.linalg.inv(basis))
        closest_vector = t @ basis        
        return closest_vector

    # Randomly generates a unimodular matrix U
    def generate_unimodular(dimension:int, iters:int=-1) -> np.array:
        identity = np.eye(dimension, dtype=int)
        if iters == -1:
            iters = dimension**2

        for iter in range(iters):
            operation = random.randint(0, 2)

            # Picks indices to perform row operations on
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, dimension-1)
                j = random.randint(0, dimension-1)
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
    
    def check_unimodular(matrix:np.array) -> bool:
        determinant = round(np.linalg.det(matrix))
        if not (determinant == 1 or determinant == -1):
            print("Not Unimodular")
            return False
        else:
            print("Unimodular")
            return True
    
    def hadamard_ratio(dimension:int, matrix:np.array) -> float:
        if matrix is None:
            return -1
        
        _, log_determinant = np.linalg.slogdet(matrix)
        determinant = np.exp(log_determinant)
        norms = np.prod(np.linalg.norm(matrix, ord=2, axis=1))
        ratio = (determinant / norms)**(1 / dimension)
        return ratio

    def check_basis(dimension:int, matrix:np.array) -> bool:
        if matrix is None:
            return False
        
        return np.linalg.matrix_rank(matrix) == dimension

    def generate_error(dimension:int, sigma: int):
        return np.random.choice(np.array([-sigma, sigma]), size=dimension,)