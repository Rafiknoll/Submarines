"""
Name:       utils.py

Purpose:    Provides utility functions for the submarine game that where not fit anywhere else

Usage:      from utils import create_multi_dimensional_array, num_to_byte, byte_to_num

Author:     Rafael Knoll
"""


def create_multi_dimensional_array(*sizes, default_value=None):
    """
    Creates a multi-dimensional array of the given sizes
    :param sizes: An iterable of sizes for the array
    :param default_value: A default value for all members of the innermost arrays (Note it better be primitive as it is
    a shallow copy!)
    :return: The multi-dimensional array
    :raises: TypeError if no dimensions were given
    """
    if len(sizes) == 0:
        raise TypeError("create_multi_dimensional_array expected at list 1 positional argument, got 0")

    ret_val = []

    if len(sizes) == 1:
        for index in range(sizes[0]):
            ret_val.append(default_value)
        return ret_val

    for index in range(sizes[0]):
        ret_val.append(create_multi_dimensional_array(*sizes[1:], default_value=default_value))
    return ret_val


def num_to_byte(num: int) -> bytes:
    """
    Converts a number to bytes representation of one byte
    :param num: The number
    :return: The byte
    """
    return num.to_bytes(1, "big")


def byte_to_num(byte: bytes) -> int:
    """
    Converts a bytes representation of one byte to a number
    :param byte: The byte
    :return: The number
    """
    return int.from_bytes(byte, "big")


def int_input(prompt=""):
    """
    Reads an integer from the user until he actually gives one
    :param prompt: The input prompt
    :return: The integer
    """
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Must input a number!")