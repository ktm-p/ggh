import numpy as np
import random
'''
    - encode(): Takes in a string message and encodes it using UTF-8. Returns a list of integers.
    - decode(): Takes in a list of integers. Decodes using UTF-8, returning a string.
    - babai_round(): Takes in a lattice basis and integer vector. Rounds the vector to the nearest lattice point.
'''
class Utils:
    def encode(message: str) -> list[int]:
        encoded = message.encode("utf8")
        return np.array(list(encoded))

    def decode(message: list[int]) -> str:
        message_bytes = bytes(message)
        return message_bytes.decode("utf8")

    # Then, we will round each of the coefficients, and this will yield us our new vector.
    def babai_round(basis: np.array , vec: np.array) -> np.array:
        # To begin with, we will want to express vec in terms of our private basis B.
        coeffs = np.linalg.solve(basis, vec)

        # Next, we round each coefficient in coeffs to the nearest integer.
        rounded_coeffs = np.round(coeffs)

        # Now, we find the resulting closest vector.
        rounded_vec = rounded_coeffs * basis
        closest_vec = []
        for i in range(0, len(rounded_vec)):
            closest_vec.append(rounded_vec[i][i])

        return np.array(closest_vec)

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
    
    def hadamard_ratio(dimension:int, matrix:np.array) -> float:
        if matrix == None:
            return -1
        
        _, log_determinant = np.linalg.slogdet(matrix)
        determinant = np.exp(log_determinant)
        norms = np.prod(np.linalg.norm(matrix, ord=2, axis=1))
        ratio = (determinant / norms)**(1 / dimension)

        print("Determinant:", determinant)
        print("Norms:", norms)
        return ratio

    def check_basis(dimension:int, matrix:np.array) -> bool:
        if matrix == None:
            return False
        
        return np.linalg.matrix_rank(matrix) == dimension

    # # Randomly generates error vector e
    # def gen_error(sigma: int):
    #     return np.array([1, -1])

    # def init(sigma:int=3, N:int=2):
    #     B = np.array([[17, 0], [0, 19]]) # Private Key
    #     U = gen_unimodular() # Unimodular Matrix

    #     Bprime = U @ B # Public Key
        
    #     return B, Bprime, U, sigma, N

    # def encrypt(message: str, Bprime: np.array) -> np.array:
    #     m = encode(message) # Encode our message into an integer vector
    #     e = gen_error(1) # Generates random noise vector e
    #     c = m @ Bprime + e # Generates ciphertext c

    #     return c

    # def decrypt(ciphertext: str, B: np.array, U: np.array) -> np.array:
    #     c = babai_round(B, ciphertext)
    #     m = c @ np.linalg.inv(B) @ np.linalg.inv(U)
    #     return decode(m.astype(int))