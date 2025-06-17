class CurlyPyTranslatorError(Exception):
    """
    Base class for CurlyPy translator errors.
    """

    pass


class CurlyPySyntaxError(CurlyPyTranslatorError):
    """
    Raised when unmatched brackets are found in the CurlyPy code.
    """

    pass
