"""
Domain-specific Exception classes for GenerIter


Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""

class GIErr(Exception):
    """
    Base class for domain-specific exceptions.
    """

class GIParameterErr(GIErr):
    """
    Class for propogating parameter errors.
    """

class GIResourceErr(GIErr):
    """
    Class for propogating resource errors.
    """

class GIValidationErr(GIErr):
    """
    Class for propogating validation errors.
    """

class GINotImplementedErr(GIErr):
    """
    Class for propogating not implemented errors.
    """
    
