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
        return fl.fmpz_mat([encoded_np.tolist()])

    def decode(message: list[int]) -> str:
        msg = [int(n) for n in message]
        message_bytes = bytes(msg)
        return message_bytes.decode("utf8")

    def conv_to_fmpz(array):
        return fl.fmpz_mat([[int(item) for item in sublist] for sublist in array.tolist()])

    def babai_round(basis: fl.fmpz_mat, vec: fl.fmpz_mat) -> fl.fmpz_mat:
        x = vec * basis.inv()
        for i in range(x.nrows()):
            for j in range(x.ncols()):
                x[i,j] = round(x[i,j])
        
        closest_vector = x * basis 
        return closest_vector

    def check_basis(matrix:fl.fmpz_mat) -> bool:
        if matrix is None:
            return False
        
        return matrix.det() != 0