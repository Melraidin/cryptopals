import base64

from Crypto.Cipher import AES


def decrypt(inp, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(inp)


if __name__ == "__main__":
    with open("set/one/challenge/seven/7.txt") as f:
        inp = base64.b64decode("".join(f.readlines()))

    print(decrypt(inp, "YELLOW SUBMARINE"))
