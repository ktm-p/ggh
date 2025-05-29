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

def babai_round(basis: list[list[int]], vec: list[int]) -> list[int]:
    rounded = []
    for row in basis:
        r = []
        for col in row:
            r.append(round(col))
        rounded.append(r)
    
    return rounded

