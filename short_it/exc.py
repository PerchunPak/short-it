"""Module for base exception."""


class ShortItException(Exception):
    """Base exception for this program."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
