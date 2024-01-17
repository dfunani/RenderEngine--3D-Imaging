# exceptions.py

"""
Module Summary: Contains custom exception classes.

Returns:
    Classes:
        ArgumentError: Raised when an invalid argument is provided.
"""


class ArgumentError(Exception):
    """
    ArgumentError Class

    Custom exception class raised when an invalid argument is provided.

    ...

    Attributes:
        message (str): A message describing the reason for the exception.

    Methods:
        __init__: Initializes the ArgumentError object with an optional custom message.
    """

    def __init__(self, message="Invalid argument(s) provided") -> None:
        """
        Initializes the ArgumentError object with an optional custom message.

        Args:
            message (str, optional): A custom message describing the reason for the exception.
                Defaults to "Invalid argument(s) provided".
        """
        self.message = message
        super().__init__(message)

class ObjectImageError(Exception):
    """
    ObjectImageError Class

    Custom exception class raised when an invalid Image file is provided.

    ...

    Attributes:
        message (str): A message describing the reason for the exception.

    Methods:
        __init__: Initializes the ObjectImageError object with an optional custom message.
    """

    def __init__(self, message="invalid Image file is provided") -> None:
        """
        Initializes the ObjectImageError object with an optional custom message.

        Args:
            message (str, optional): A custom message describing the reason for the exception.
                Defaults to "invalid Image file is provided".
        """
        self.message = message
        super().__init__(message)
