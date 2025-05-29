def encode(plaintext: str) -> list[int]:
    res = plaintext.encode("utf8")
    return res

txt = "Hello World!"
print("Text:", txt)
enc = encode(txt)
print("Encoded:", enc)