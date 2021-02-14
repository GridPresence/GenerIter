#!/usr/bin/env python3
"""
App that is used to generate code stubs for local algorithmic development.

    .. code:: bash

       usage: generalg [-h] -A A -M M -L L
       
       optional arguments:
          -h, --help  show this help message and exit
          -A A        Algorithm name
          -M M        Module name
          -L L        Library name

Thus:

    .. code:: bash

       generalg -L testlib -M testmod -A testalg

will ensure that a directory named **testlib** is created.

Within **testlib**, the app ensures that the **__init__.py** and **Testmod.py** files exist.

The **Testmod.py** will contain:

    .. code:: python

       from GenerIter.process import Process

       class Testmod(Process):
       
           def __init__(self):
               super().__init__()
       
       
           def testalg(self):
               print("Executing testalg")
               # Your code goes here


"""
import argparse
from pathlib import Path

from GenerIter.app.clibase import CLIBase
from GenerIter.selector import Selector
import GenerIter.excepts as gix
from GenerIter.util import debug

class Algorithm(CLIBase):

    klass_template = '''from GenerIter.process import Process

class {KLASS}(Process):

    def __init__(self):
        super().__init__()

'''

    alg_template = '''
    def {ALG}(self):
        print("Executing {ALG}")
        # Your code goes here

'''

    def _init_(self):
        super(Algorithm, self).__init__()


    def parseArguments(self):
        # Set up positional and optional arguments
        parser = argparse.ArgumentParser()
        # Zero or more -I parameters are allowed
        parser.add_argument("-A", help="Algorithm name",
                            action='store', required=True)
        # Zero or more -I parameters are allowed
        parser.add_argument("-M", help="Module name",
                            action='store', required=True)
        # This is a mandatory output name parameter.
        parser.add_argument("-L", help="Library name",
                            action='store', required=True)
        
        # Parse the command line as supplied
        args = parser.parse_args()
        # Set up the member values according to the command line options
        self._library = args.L.lower()
        self._module = args.M.lower()
        self._klass = self._module.capitalize()
        self._algorithm = args.A.lower()

    def build_lib(self):
        lib = Path(self._library)
        lib.mkdir(parents=True, exist_ok=True)
        init = lib / '__init__.py'
        if init.exists() is False:
            init.touch()

    def build_class(self):
        prog = '{0}.py'.format(self._klass)
        mod = Path(self._library) / prog
        if mod.exists() is False:
            #mod.open(mode='w')
            mod.write_text(self.klass_template.format(KLASS=self._klass))

    def build_method(self):
        prog = '{0}.py'.format(self._klass)
        mod = Path(self._library) / prog
        modfile = open(mod, mode='a+')
        modfile.write(self.alg_template.format(ALG=self._algorithm))
            
    def process(self):
        self.build_lib()
        self.build_class()
        self.build_method()
