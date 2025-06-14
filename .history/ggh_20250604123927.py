import math
import numpy as np
import random
from flint import fmpz_mat, fmpz, fmpq, fmpq_mat
from Utils.utils import Utils
import time

random.seed(69)
np.random.seed(69)
class GGH:
    def __init__(self, dimension:int=2, sigma:int=3, thresh:int=4):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = self.generate_private_key_rectangular()
        self.unimodular = Utils.generate_unimodular(self.dimension)
        self.public_key = self.generate_public_key()

    def generate_private_key(self) -> np.array:
        basis = None
        # Checks if set of vectors is a basis and has a sufficiently high Hadamard Ratio
        while (not Utils.check_basis(self.dimension, basis)) or (Utils.hadamard_ratio(self.dimension, basis) < 0.75):
            basis = np.random.choice(np.array([-self.thresh, self.thresh]), size=(self.dimension, self.dimension))

        return basis

    def generate_private_key_rectangular(self) -> np.array:
        k = self.thresh * math.ceil(math.sqrt(self.dimension))
        identity = np.eye(self.dimension, dtype=int)
        basis = None
        while not Utils.check_basis(self.dimension, basis):
            r = np.random.choice(np.array([-self.thresh, self.thresh]), size=(self.dimension, self.dimension))
            basis = r + (k * identity)
        
        print("Hadamard Ratio", Utils.hadamard_ratio(self.dimension, basis))
        return basis
    
    def generate_public_key(self) -> np.array:
        return self.unimodular @ self.private_key
    
    def generate_public_key_mixing(self) -> np.array:
        T = np.eye(dim)
        x = np.eye(1, dim)
        choices = np.array([-1, 0, 1])
        weights = np.array([1, 5, 1])


        return
    
    def encrypt(self, message:str) -> np.array:
        encoded = Utils.encode(message)
        print("Encoded", encoded)
        print("mB", encoded @ self.public_key)
        error_vector = Utils.generate_error(self.dimension, self.sigma)
        ciphertext = encoded @ self.public_key + error_vector
        print("Ciphertext", ciphertext)
        return ciphertext
    
    def decrypt(self, ciphertext:np.array) -> str:
        closest_vector = Utils.babai_round(self.private_key, ciphertext)
        print("mB", closest_vector)
        message = np.round(closest_vector @ np.linalg.inv(self.public_key))
        print("Encoded", message)
        return Utils.decode(message.astype(int))

    def attacker_decrypt(self, ciphertext:np.array) -> str:
        closest_vector = Utils.babai_round(self.public_key, ciphertext)
        message = np.round(closest_vector @ np.linalg.inv(self.public_key))
        return Utils.decode(message.astype(int))

message = "hello! how are you? i am very good! and you are? hahaha, i am glad! why didn't it...?"
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
# faulty_decrypted = inst.attacker_decrypt(encrypted)

print("Message:", message)
print("Encrypt:", encrypted)
print("Decrypt:", decryptyed)
# print("Attacker Attempt:", faulty_decrypted)

print("Initialization:", init_end - init_start)
print("Encryption:", enc_end - enc_start)
print("Decryption:", dec_end - dec_start)