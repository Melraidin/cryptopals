import base64

from util.grouper import grouper


def fixed_xor(x, y):
    """
    Xor two strings of hex values and return results as a hex string.

    >>> fixed_xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965")
    '746865206b696420646f6e277420706c6179'
    """

    return "".join(
        "%02x" % (int("".join(xa), 16) ^ int("".join(ya), 16))
        for xa, ya in zip(grouper(x, 2), grouper(y, 2)))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
