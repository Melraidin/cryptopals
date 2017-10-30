import itertools


def encrypt_str(inp, key):
    """
    Applies repeating key Xor to inp using given key.

    >>> encrypt_str("Burning 'em, if you ain't quick and nimble\\nI go crazy when I hear a cymbal", "ICE")
    '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
    """

    return "".join("%02x" % x for x in encrypt([ord(y) for y in inp], [ord(z) for z in key]))


def encrypt(inp, key):
    return [x[0] ^ x[1] for x in zip(inp, itertools.cycle(key))]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
