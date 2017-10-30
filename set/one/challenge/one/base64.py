import base64

from util.grouper import grouper


def encode_hex_to_base64(h):
    """
    Encode a hex string as base 64.
    """

    return base64.b64encode("".join(chr(int(x + y, 16)) for x, y in grouper(h, 2)))
