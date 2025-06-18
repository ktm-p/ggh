import numpy as np
import flint as fl
import random
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
        encoded_np = np.array(list(encoded))
        # print(encoded_np.tolist())
        print(encoded_np)
        return fl.fmpz_mat([encoded_np.tolist()])

    def decode(message: list[int]) -> str:
        print("message")
        msg = [int(n) for n in message]
        message_bytes = bytes(msg)
        return message_bytes.decode("utf8")

    def conv_to_fmpz(array):
        return fl.fmpz_mat([[int(item) for item in sublist] for sublist in array.tolist()])

    def babai_round(basis: fl.fmpz_mat, vec: fl.fmpz_mat) -> fl.fmpz_mat:
        print("Babai's Rounding.")
        x = vec * basis.inv()
        print("Calculated inverse.")
        for i in range(x.nrows()):
            for j in range(x.ncols()):
                x[i,j] = round(x[i,j])
        
        closest_vector = x * basis 
        print("Babai finished.")
        return closest_vector
    
    def check_unimodular(matrix:np.ndarray) -> bool:
        determinant = round(np.linalg.det(matrix))
        if not (determinant == 1 or determinant == -1):
            print("Not Unimodular")
            return False
        else:
            print("Unimodular")
            return True
    
    def hadamard_ratio(dimension:int, matrix:np.ndarray) -> float:
        if matrix is None:
            return -1
        
        _, log_determinant = np.linalg.slogdet(matrix)
        determinant = np.exp(log_determinant)
        norms = np.prod(np.linalg.norm(matrix, ord=2, axis=1))
        ratio = (determinant / norms)**(1 / dimension)
        return ratio

    def check_basis(matrix:fl.fmpz_mat) -> bool:
        if matrix is None:
            return False
        
        return matrix.det() != 0

    def generate_error(dimension:int, sigma: int):
        err = [random.choice([-sigma, sigma]) for _ in range(dimension)]
        return fl.fmpz_mat([err])