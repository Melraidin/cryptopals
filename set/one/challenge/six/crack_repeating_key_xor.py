import base64
import itertools

from util.grouper import grouper
from set.one.challenge.three import single_byte_decrypt
from set.one.challenge.five import repeating_key_xor


def crack(inp, key_size):
    """
    Attempt to crack repeating key Xor.
    """

    key_size = find_key_size(inp)

    # Transpose: group the first byte of each block, then the second
    # byte of each block, etc.
    grouped = [list(x) for x in zip(*grouper(inp, key_size, fillvalue=0))]

    key = []

    for g in grouped:
        res = single_byte_decrypt.attempt_decrypt(g)
        key.append(res[2])

    return key


def find_key_size(inp):
    """
    Attempts to find the key size given an Xor encrypted string.

    >>> find_key_size([ord(x) for x in base64.b64decode("HUIfTQsPAh9PE048GmllH0kcDk4TAQsHThsBFkU2AB4BSWQgVB0dQzNTTmVSBgBHVBwNRU0HBAxTEjwMHghJGgkRTxRMIRpHKwAFHUdZEQQ=")])
    5
    """

    # Key size, normalized Hamming dis;:tance.
    best = (1, 99999.99)

    res = []

    for size in xrange(1, 40):
        norm = 0.0

        j = 0
        ham = 0
        for i in xrange(0, len(inp), size * 2):
            x1 = inp[i:i + size]
            x2 = inp[i + size:i + size * 2]

            if len(x2) < size:
                break

            ham += hamming(x1, x2)
            j += 1

        norm = ham / float(j * size)
        res.append((size, norm))
        if norm < best[1]:
            best = (size, norm)

    return best[0]


def hamming_str(a, b):
    """
    Returns Hamming distance between two strings.

    >>> hamming_str("this is a test", "wokka wokka!!!")
    37
    """

    return hamming([ord(x) for x in a], [ord(x) for x in b])


def hamming(a, b):
    """
    Returns Hamming distance between two lists.
    """

    return sum(
        bin(x[0] ^ x[1]).count("1")
        for x in itertools.izip_longest(a, b, fillvalue=0))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open("set/one/challenge/six/6.txt") as f:
        body = [ord(x) for x in base64.b64decode("".join(f.readlines()))]

    key = crack(body, 29)

    print("Key: %s\n" % key)
    print("".join(chr(x) for x in repeating_key_xor.encrypt(body, key)))
