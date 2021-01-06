"""

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import GenerIter.excepts as gix

class CLIBase():

    def __init__(self):
        self.parseArguments()
        self.process()

    def parseArguments(self):
        raise gix.GINotImplementedErr("The method parseArguments() is not implemented on this object.")

    def process(self):
        raise gix.GINotImplementedErr("The method process() is not implemented on this object.")
