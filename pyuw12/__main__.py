from pyuw12_backend import uw12_interface


def get_result():
    """
    An example function which calls the UW12 interface

    Returns:
        int: Sum of two integers
    """
    return uw12_interface.uw12_energy(1, 2)


if __name__ == "__main__":
    result = get_result()
    print(result)
