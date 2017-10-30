import itertools


def grouper(iterable, n, fillvalue=None):
    """
    Take elements from an iterable in groups of size n.
    """

    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)
