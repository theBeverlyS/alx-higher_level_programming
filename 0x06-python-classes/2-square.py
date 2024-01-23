#!/usr/bin/python3

"""Define a class Square."""

class Square:
    """Represent a Square."""

    def __init__(self, size=0):
        """Initialize a new Square.

        Args:
        size (int): The size of a new square.
        """
        if not instance(size, int):
            raise TypeError("size must be an integer")
        elif size < 0:
            raise ValueError("size must be >=0"),
        self._size = size

