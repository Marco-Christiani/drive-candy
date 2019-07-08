class Error(Exception):
    """
    Base class for exceptions in this module.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return f'\n\t- {self.expression} failed.\n\t- {self.message}'


class TokenRequired(Error):
    pass


class InvalidTimeToLive(Error):
    pass


# ------------------------------------------------------------------------------

class EnvironmentVariableNotSet(Error):
    def __str__(self):
        return f'\n\t- {self.expression}\n\t- {self.message}'
