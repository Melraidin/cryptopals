import collections

from util.grouper import grouper


def select_aes_ecb(inp):
    """
    Filter list inp to include only elements that may be AES ECB
    encrypted.

    Args:
        inp: List of inputs.

    Returns:
        List of input elements that may be AES ECB encrypted.
    """

    counts = [(x, detect_aes_ecb(x)) for x in inp]

    return [x[0] for x in counts if x[1] > 1]


def detect_aes_ecb(inp):
    """
    Find repeated blocks in inp.
    """

    counts = collections.defaultdict(lambda: 0)
    for g in grouper(inp, 16):
        counts[g] += 1

    return sum([c for c in counts.values() if c > 1])


if __name__ == "__main__":
    with open("set/one/challenge/eight/8.txt") as inp:
        dat = []
        for line in inp.readlines():
            dat.append([int("".join(x), 16) for x in grouper(line.strip(), 2)])

    for x in select_aes_ecb(dat):
        print("".join("%02x" % y for y in x))
