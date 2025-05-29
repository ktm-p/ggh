'''
    encode(): Takes in a string message and encodes it using UTF-8. Returns a list of integers.
    decde(): Takes in a list of integers. Decodes using UTF-8, returning a string.
'''
def encode(message: str) -> list[int]:
    res = message.encode("utf8")
    return list(res)

def decode(message: list[int]) -> str:
    res = bytes(message)
    return res.decode("utf8")

