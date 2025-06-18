import math
import numpy as np
import sympy as sp
import random
import flint as fl
from Utils.utils import Utils
import time

random.seed(69)
np.random.seed(69)

class GGH:
    def __init__(self, dimension:int, sigma:int=3, thresh:int=4):
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = self.generate_private_key()
        self.unimodular = self.generate_unimodular()
        self.public_key = self.generate_public_key()

    # Randomly generates a unimodular matrix U
    def generate_unimodular(self, iters:int=2) -> fl.fmpz_mat:
        x = sp.zeros(1, self.dimension)
        identity = sp.eye(self.dimension)

        weights = [1, 5, 1]
        vals = [-1, 0, 1]

        for iter in range(iters):
            rows = list(range(dim))
            random.shuffle(rows)
            for i in rows:
                x[0, i] = 1
                for j in range(self.dimension):
                    if j != i:
                        x[0, j] = random.choices(vals, weights=weights)[0]

                new_row = x * identity
                for j in range(dim):
                    identity[i, j] = new_row[0, j]
                
                x[0, i] = 0
        
        return Utils.conv_to_fmpz(identity)

    def generate_private_key(self) -> fl.fmpz_mat:
        k = fl.fmpz(self.thresh * math.ceil(math.sqrt(self.dimension)))
        identity = Utils.conv_to_fmpz(np.eye(self.dimension))
        basis = None
        while not Utils.check_basis(basis):
            r = fl.fmpz_mat([[random.randint(-self.thresh, self.thresh) for _ in range(self.dimension)] for _ in range(self.dimension)])
            basis = r + (k * identity)
        
        return fl.fmpz_mat(basis)
    
    def generate_public_key(self) -> np.array:
        return self.unimodular * self.private_key
    
    def encrypt(self, message:str) -> np.array:
        print("Encrypting.")
        encoded = Utils.encode(message)
        # print("Encoded", encoded)
        # print("mB", encoded * self.public_key)
        error_vector = Utils.generate_error(self.dimension, self.sigma)
        ciphertext = encoded * self.public_key + error_vector
        # print("Ciphertext", ciphertext)
        print("Encrypted.")
        return ciphertext
    
    def decrypt(self, ciphertext:np.array) -> str:
        print("Decrypting.")
        closest_vector = Utils.babai_round(self.private_key, ciphertext)
        message = closest_vector * self.public_key.inv()
        return Utils.decode(message)

message = "a"*300
dim = len(message)
print("Dimension:", dim)
init_start = time.time()
inst = GGH(dimension=dim)
init_end = time.time()

enc_start = time.time()
encrypted = inst.encrypt(message)
enc_end = dec_start = time.time()
decryptyed = inst.decrypt(encrypted)
dec_end = time.time()

print("Message:", message)
# print("Encrypt:", encrypted)
print("Decrypt:", decryptyed)

print("Initialization:", init_end - init_start)
print("Encryption:", enc_end - enc_start)
print("Decryption:", dec_end - dec_start)