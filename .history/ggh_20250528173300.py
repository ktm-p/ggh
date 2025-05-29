import numpy as np
import random
from Utils.utils import Utils

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
        print("Encoded:", encoded)
        error_vector = Utils.generate_error(self.dimension, self.sigma)
        print("Error:", error_vector)
        ciphertext = encoded @ self.public_key + error_vector
        return ciphertext

    
    def decrypt(self, ciphertext:np.array) -> str:
        closest_vector = Utils.babai_round(self.private_key, ciphertext)
        message = closest_vector @ np.linalg.inv(self.private_key) @ np.linalg.inv(self.unimodular)
        # return Utils.decode(message.astype(int))
        return message

inst = GGH(dimension=3)
print("Public Key:", inst.public_key)
print("Hadamard Ratio:", Utils.hadamard_ratio(inst.dimension, inst.public_key))

message = "hey"
encrypted = inst.encrypt(message)
decryptyed = inst.decrypt(encrypted)

print("Message:", message)
print("Encrypt:", encrypted)
print("Decrypt:", decryptyed)

