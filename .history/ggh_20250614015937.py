import math
import numpy as np
import random
import flint as fl
from Utils.utils import Utils
import time

random.seed(69)
np.random.seed(69)

class GGH:
    def __init__(self, dimension:int, sigma:int=3, thresh:int=4):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = self.generate_private_key_rectangular()
        self.unimodular = Utils.generate_unimodular(self.dimension)
        self.public_key = self.generate_public_key()

        self.private_inv = np.linalg.inv(self.private_key)
        self.public_inv = np.linalg.inv(self.public_key)

        print(self.private_inv)
        print(self.public_inv)

        self.private_key = Utils.np_to_fl(self.private_key)
        self.public_key = Utils.np_to_fl(self.public_key)
        self.unimodular = Utils.np_to_fl(self.unimodular)
        self.private_inv = Utils.np_to_flq(self.private_inv)
        self.public_inv = Utils.np_to_flq(self.public_inv)


    def generate_private_key(self) -> fl.fmpz_mat:
        basis = None
        # Checks if set of vectors is a basis and has a sufficiently high Hadamard Ratio
        while (not Utils.check_basis(self.dimension, basis)) or (Utils.hadamard_ratio(self.dimension, basis) < 0.75):
            basis = np.random.choice(np.array([-self.thresh, self.thresh]), size=(self.dimension, self.dimension))

        return basis

    def generate_private_key_rectangular(self) -> fl.fmpz_mat:
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
        error_vector = Utils.generate_error(self.dimension, self.sigma)
        ciphertext = encoded * self.public_key + error_vector
        return ciphertext
    
    def decrypt(self, ciphertext:np.array) -> str:
        s = time.time()
        closest_vector = Utils.babai_round(self.private_key, self.private_inv, ciphertext)
        e = time.time()
        print("Babai's", e-s)
        # print("mB", closest_vector)
        s = time.time()
        message = closest_vector * self.public_inv
        e = time.time()
        print("Inverse:", e-s)
        # print("Encoded", message)
        return Utils.decode(message)

    def attacker_decrypt(self, ciphertext:np.array) -> str:
        closest_vector = Utils.babai_round(self.public_key, self.public_inv, ciphertext)
        message = closest_vector * self.public_key.inv()
        return Utils.decode(message)

message = "gfttclyqiibaivqvzmgoldyffzmzhcpjpjmnplrwbnfprnkmkrepdfkgvxpvcjbooixtcqmtaogbxeolrthuoqlevpqfomzfaxkikfpjpvesnzjzlqxlreimbajvuzffirugmdlokmcsojrzduknvblnkdmxsawo"
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
try:
    attacker_decrypted = inst.attacker_decrypt(encrypted)
except ValueError:
    attacker_decrypted = "Decryption Error"

print("Message:", message)
# print("Encrypt:", encrypted)
print("Decrypt:", decryptyed)
print("Correct Decryption?", message == decryptyed)
print("Attacker Decrypt:", attacker_decrypted)

print("Initialization:", init_end - init_start)
print("Encryption:", enc_end - enc_start)
print("Decryption:", dec_end - dec_start)