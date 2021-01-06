#!/usr/bin/env python3
"""
App to catalogue and select source files into a configuration.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import argparse

from GenerIter.app.clibase import CLIBase
from GenerIter.selector import Selector
import GenerIter.excepts as gix
from GenerIter.util import debug

class Inventory(CLIBase):

    def _init_(self):
        super(Inventory, self).__init__()


    def parseArguments(self):
        # Set up positional and optional arguments
        parser = argparse.ArgumentParser()
        # Zero or more -I parameters are allowed
        parser.add_argument("-I", help="Source for inclusion in searches",
                            action='append')
        # Zero or more -I parameters are allowed
        parser.add_argument("-L", help="Source for inclusion in loads",
                            action='append')
        # This is a mandatory output name parameter.
        parser.add_argument("-o", help="Output file root name",
                            action='store', required=True)
        
        # Parse the command line as supplied
        args = parser.parse_args()
        # Set up the member values according to the command line options
        self._includes = args.I # This is a list
        self._loads = args.L # This is a list
        self._outfile = "{0}.json".format(args.o)


    def process(self):
        sel=Selector()
        if self._includes is not None:
            # Iterate over the search paths first
            for srcdir in self._includes:
                sel.search(srcdir)
        if self._loads is not None:
            # Iterate over any load files next
            for load in self._loads:
                sel.load(load)
        # Write it all out as a JSON file
        with open(self._outfile, "w") as of:
            of.write(str(sel))

#if __name__ == '__main__':
#    app = Inventory()
