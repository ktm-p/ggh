def encode(message: str) -> list[int]:
    res = message.encode("utf8")
    return list(res)

def decode(message: list[int]) -> str:
    res = bytes(message)
    return res.decode("utf8")

txt = "Hello World!"
print("Text:", txt)
enc = encode(txt)
print("Encoded:", enc)
dec = decode(enc)
print("Decoded:", dec)