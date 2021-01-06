"""
Class that constructs the correct processor object.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
from GenerIter.selector import Selector
from GenerIter.config import Config
import GenerIter.excepts as robox
from GenerIter.util import debug

class ProcessorFactory():

    def __init__(self, vname, pname, fname, procmodule='GenerIter.processor'):
        self._vname = vname
        self._pname = pname
        self._method = None
        self._klass = None
        
        if self._vname is not None:
            modspec = '{0}.{1}'.format(procmodule, self._vname)
            try:
                mod = __import__(modspec, fromlist=[self._vname])
            except ImportError:
                raise ImportError('Could not import {0}.{1}'.format(modspec, self._vname))
            # Load the class from the module
            klass = getattr(mod, self._vname)
            # Create an object instance
            self._klass = klass()
            if self._klass is None:
                raise ImportError('Failed to instantiate {0}.{1}.{1}'.format(modspec, self._vname))
            # If we got here, we have a class instantiation
            # Let's see if we can get a reference to a method
            try:
                print("{0}.{1}()".format(self._vname, self._pname))
                self._method = getattr(self._klass, self._pname)
            except AttributeError:
                raise AttributeError('Could not obtain reference to {0}.{1}'.format(self._name, self._pname))

    @property
    def klass(self):
        return self._klass

    @property
    def method(self):
        return self._method

    def setMethod(self, fname):
        self._method = None
        if self._klass is not None:
            try:
                self._method = getattr(self._klass, fname)
            except AttributeError:
                print('Could not obtain {0}.{1}'.format(self._name, fname))
                sys.exit(-1)
        return self._method

    def configure(self, invent, config, dest, form):
        self._klass.configure(inventory=invent, configuration=config, destination=dest, forrmat=form)

    def process(self):
        self._method()
    
