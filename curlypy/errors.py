
class BrythonTranslatorError(Exception):
    """
    Base class for all exceptions raised by the BrythonTranslator class.
    """
    pass


# Error definitions
class UnmatchedBracketsError(BrythonTranslatorError):
    """
    Raised when unmatched brackets are found in the Brython code.
    """
    pass

class UnmatchedQuotesError(BrythonTranslatorError):
    """
    Raised when unmatched quotes are found in the Brython code.
    """
    pass