"""Exceptions used throughout package"""


class FlintaiError(Exception):
    """Base worldgen Error"""

class CommandError(FlintaiError):
    """Raised when there is an error in command-line arguments"""

class BadCommand(FlintaiError):
    """Raised when a command is not found"""