import collections
import string

from util.grouper import grouper

# string.printable includes some characters we don't want; exclude
# them.
_PRINTABLE_CHARS = [x for x in string.printable if x not in "\x0b\x0c"]

_COMMON_PUNCTUATION = ",.()!$%:?'\""
_UNCOMMON_PUNCTUATION = "~{}"

# English letter frequencies from:
# http://en.algoritmy.net/article/40379/Letter-frequency-English
_ENGLISH_FREQUENCIES = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]


def attempt_decrypt(inp):
    """
    Attempt to decrypt a hex string with single character Xor
    encryption.
    """

    # Best key, score, and decrypted string so far.
    best = (0, 99999.99, "")

    res = []

    for k in xrange(0, 255):
        decrypted = xor_decrypt(inp, k)
        score = find_frequency_fit(decrypted)
        if score is None:
            continue

        orig_score = score

        printable = 0
        for x in decrypted:
            if chr(x) in _PRINTABLE_CHARS:
                printable += 1

        if printable < len(inp) / 2:
            continue

        res.append((k, score, decrypted, orig_score))
        if score < best[1]:
            best = (k, score, decrypted)

    return best[2], best[1], best[0]


def xor_decrypt(inp, key):
    """
    Decrypt a list with a single-byte Xor key.
    """

    return [x ^ key for x in inp]


def find_frequency_fit(inp):
    """
    Returns the most common letter in inp if it's a common English
    letter.
    """

    counts = collections.defaultdict(lambda: 0)
    for c in inp:
        counts[c] += 1

    frequencies = sorted(counts.keys(), key=lambda x: counts[x])

    if chr(frequencies[-1]) in 'etaoinETAOIN ':
        return frequencies[-1]
    else:
        return None


def find_frequency_fit_old(inp):
    """
    Score the string based on letter frequency in English.

    This appears to function properly but doesn't work well with the
    challenges on Cryptopals. A simpler solution worked fine, see
    find_frequency_fit().
    """

    ord_a = ord("a")

    counts = collections.defaultdict(lambda: 0)
    ignored = 0
    for x in inp:
        if x >= ord("a") and x <= ord("z"):
            counts[x - ord_a] += 1
        elif x >= ord("A") and x <= ord("Z"):
            # Convert to lowercase.
            counts[x + 32 - ord_a] += 1
        else:
            ignored += 1

    used_length = len(inp) - ignored
    if used_length == 0:
        return None

    chi2 = 0.0
    for k, c in counts.iteritems():
        expected = used_length * _ENGLISH_FREQUENCIES[k]
        diff = c - expected
        chi2 += diff * diff / expected

    # Boost score based on letter count.
    boost = 1.0
    per_char = 1.0 / len(decrypted)
    ignored = 0
    for x in decrypted:
        if chr(x) in string.letters:
            boost -= per_char
        elif chr(x) in string.whitespace:
            pass
        elif chr(x) in _COMMON_PUNCTUATION:
            boost -= per_char
        elif chr(x) in _UNCOMMON_PUNCTUATION:
            boost += per_char * 6
        else:
            ignored += 1

    score = chi2 * boost
    if ignored > 0:
        score *= 1.0 + (float(ignored) / len(decrypted))

    return score


if __name__ == "__main__":
    inp = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    enc = [int("".join(x), 16) for x in grouper(inp, 2)]

    print("".join(chr(x) for x in attempt_decrypt(enc)[0]))
