#!/usr/bin/env python3
"""
App that is used to subcategorise a sample set according to a string search parameter.

The app will iterate through all the files in the current directory looking for files containing the category search pattern substring (the **-C** argument).
       
If the category search pattern is found in a filename, the file is moved into a subdirectory, which will be created if necessary. The 
name of the subdirectory will either correspond to the category search string or is specified by the **-D** argument.

Thus:

    .. code:: bash

       genercat -C Drums
        
and

    .. code:: bash

       genercat -C Drums -D Drums

are functionally identical, whereas

    .. code:: bash
        
       genercat -C Drums - D Percussion

puts the same files into a different subdirectory.

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
        """Parses the CLI arguments for the app.

        .. code:: bash

           usage: genercat [-h] -C C [-D D]
           
           optional arguments:
           -h, --help  show this help message and exit
           -C C        Category search pattern
           -D D        Destination category name

        """
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
        """The execution function for the app.

        The basic flow:

        #. A destination subdirectory is created, unless it already exists. 

        #. The app then examines all the files in the current directory.
        
        #. If the specfied category search substring is found in the filename, that file is moved into the subdirectory.
        """
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
