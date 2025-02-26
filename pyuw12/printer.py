def printVal(text: str, value, verbose=1, **kwargs):
    """
    Print a formatted value if verbose > 0

    Args:
        text (str): Value name
        value: Value
        verbose (int): Verbosity level
    """
    if verbose > 0:
        print("{0:<32} {1}".format(text, value), **kwargs)
