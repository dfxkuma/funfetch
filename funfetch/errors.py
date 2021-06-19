class FunFetchException(Exception):
    """This is the basic error class for Funfetch"""

    pass


class ConnectionError(FunFetchException):
    """This error occurs when the server you are trying to connect to cannot be reached."""

    pass


class CompileError(FunFetchException):
    """This is a problem that occurs when compiling the code."""

    pass
