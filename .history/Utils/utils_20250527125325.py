import numpy as np

'''
    - encode(): Takes in a string message and encodes it using UTF-8. Returns a list of integers.
    - decode(): Takes in a list of integers. Decodes using UTF-8, returning a string.
    - babai_round(): Takes in a lattice basis and integer vector. Rounds the vector to the nearest lattice point.
'''
def encode(message: str) -> list[int]:
    res = message.encode("utf8")
    return np.array(list(res))

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
    closest_vec = np.sum(rounded_coeffs * basis)
    
    return closest_vec

# Randomly generates a unimodular matrix U
def gen_unimodular():
    return np.array([[2, 3], [3, 5]])

# Randomly generates error vector e
def gen_error(sigma: int):
    return np.array([1, -1])

def init(sigma:int=3, N:int=2):
    B = np.array([[17, 0], [0, 19]]) # Private Key
    U = gen_unimodular() # Unimodular Matrix

    Bprime = U @ B # Public Key
    
    return B, Bprime, U, sigma, N

def encrypt(message: str, Bprime: np.array) -> np.array:
    m = encode(message) # Encode our message into an integer vector
    e = gen_error(1) # Generates random noise vector e
    c = m @ Bprime + e # Generates ciphertext c

    return c

def decrypt(ciphertext: str, B: np.array, U: np.array) -> np.array:
    ...

msg = "Hi"
enc = encode(msg)
print("Message:", msg)
print("Encoded:", enc)
dec = decode(enc)
print("Decoded:", dec)

B, Bprime, U, sigma, N = init()
print("B:", B)
print("Bprime", Bprime)
print("U:", U)

c = encrypt(msg, Bprime)
print("c", c)