#!/usr/bin/env python3
"""
Subcategorise a sample set according to a string search parameter.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import argparse
import pathlib

from GenerIter.app.clibase import CLIBase
import GenerIter.excepts as gix
from GenerIter.util import debug, mkdir_p

class Categorise(CLIBase):

    def _init_(self):
        super(Categorise, self).__init__()
        self._cat = None
        self._dest = None


    def parseArguments(self):
        # Set up positional and optional arguments
        parser = argparse.ArgumentParser()
        # This is the target string for the category
        parser.add_argument("-C", help="Category search pattern",
                            action='store', required=True)
        parser.add_argument("-D", help="Destination category name",
                            action='store')
        
        # Parse the command line as supplied
        args = parser.parse_args()
        # Set up the member value according to the command line options
        self._cat = args.C
        self._dest = args.D
        if self._cat is not None:
            if self._dest is None:
                self._dest = self._cat
        


    def process(self):
        mkdir_p(self._dest)
        # define the path
        currentDirectory = pathlib.Path('.')

        for currentFile in currentDirectory.iterdir():
            if self._cat in currentFile.stem:
                if currentFile.is_file() is True:
                    target = pathlib.Path(self._dest, currentFile)
                    print(target)
                    currentFile = currentFile.replace(target)
                    print(currentFile)

#if __name__ == '__main__':
#    app = Inventory()
