"""
Abstract base class for Command Line Interface apps in the GenerIter ecosystem

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import GenerIter.excepts as gix

class CLIBase():

    def __init__(self):
        """
        Common core initialisation sequence for all CLIBase objects.

        First all the command line options and arguments are parsed and validated.
        Secondly, the application processing function is executed.
        """
        self.parseArguments()
        self.process()

    def parseArguments(self):
        """
        There is no implementation of this function for the abstract base class.

        Raises:
            GenerIter.excepts.GINotImplementedErr

        """
        raise gix.GINotImplementedErr("The method parseArguments() is not implemented on this object.")

    def process(self):
        """
        There is no implementation of this function for the abstract base class.

        Raises:
            GenerIter.excepts.GINotImplementedErr

        """
        raise gix.GINotImplementedErr("The method process() is not implemented on this object.")
