import numpy as np
import random
from Utils.utils import Utils
import time

random.seed(69)

class GGH:
    def __init__(self, dimension:int=2, sigma:int=3, thresh:int=1000):
        # Pre-determined values for N (the dimension) and sigma (the error size)
        self.dimension = dimension
        self.sigma = sigma
        self.thresh = thresh

        self.private_key = Utils.generate_private_key(self.dimension, self.thresh)
        self.unimodular = Utils.generate_unimodular(self.dimension, 100)
        self.public_key = Utils.generate_public_key(self.unimodular, self.private_key)
    
    def encrypt(self, message:str) -> np.array:
        encoded = Utils.encode(message)
        error_vector = Utils.generate_error(self.dimension, self.sigma)
        ciphertext = encoded @ self.public_key + error_vector
        return ciphertext
    
    def decrypt(self, ciphertext:np.array) -> str:
        closest_vector = Utils.babai_round(self.public_key, ciphertext)
        message = np.round(closest_vector @ np.linalg.inv(self.private_key) @ np.linalg.inv(self.unimodular))
        return Utils.decode(message.astype(int))

message = "hello!"
dim = len(message)
init_start = time.time()
inst = GGH(dimension=dim)
init_end = time.time()

enc_start = time.time()
encrypted = inst.encrypt(message)
enc_end = dec_start = time.time()
decryptyed = inst.decrypt(encrypted)
dec_end = time.time()

print("Message:", message)
print("Encrypt:", encrypted)
print("Decrypt:", decryptyed)

print("Initialization:", init_end - init_start)
print("Encryption:", enc_end - enc_start)
print("Decryption:", dec_end - dec_start)