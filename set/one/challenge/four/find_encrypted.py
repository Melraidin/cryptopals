from set.one.challenge.three import single_byte_decrypt


if __name__ == "__main__":
    with open("set/one/challenge/four/4.txt") as f:
        dat = f.readlines()

    res = [single_byte_decrypt.attempt_decrypt(x.strip()) for x in dat]
    for attempt in sorted(res, key=lambda x: x[1]):
        plaintext = "".join(chr(x) for x in attempt[0])
        if plaintext != "":
            print(plaintext)
