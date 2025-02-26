def printVal(text: str, value, **kwargs):
    """
    Print a formatted value

    Args:
        text (str): Value name
        value: Value
    """
    print("{0:<32} {1}".format(text, value), **kwargs)
