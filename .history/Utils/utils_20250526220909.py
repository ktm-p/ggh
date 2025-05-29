import numpy as np

'''
    - encode(): Takes in a string message and encodes it using UTF-8. Returns a list of integers.
    - decode(): Takes in a list of integers. Decodes using UTF-8, returning a string.
    - babai_round(): Takes in a lattice basis and integer vector. Rounds the vector to the nearest lattice point.
'''
def encode(message: str) -> list[int]:
    res = message.encode("utf8")
    return list(res)

def decode(message: list[int]) -> str:
    res = bytes(message)
    return res.decode("utf8")

# Then, we will round each of the coefficients, and this will yield us our new vector.
def babai_round(basis: np.array , vec: np.array) -> np.array:
    # To begin with, we will want to express vec in terms of our private basis B.
    coeffs = np.linalg.solve(basis, vec)

    # Next, we round each coefficient in coeffs to the nearest integer.
    rounded_coeffs = np.round(coeffs)


    # Now, we find the resulting closest vector.

    
    return rounded

