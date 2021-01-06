"""
Class to configure generator algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""

import os
import json
import GenerIter.excepts as robox
from GenerIter.util import jStr, debug, debug_except

class Config():
    
    def __init__(self, confpath=None):
        self._data = {}
        if confpath is not None:
            self.load(inpath=confpath)

    def load(self, inpath):
        if inpath is not None:
            with open(inpath) as fp:
                self._data = json.load(fp)

    def subcats(self):
        retval = []
        for key in self._data:
            if key != "Globals":
                retval.append(key)
        return retval

    def __str__(self):
        return jStr(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        self._data[key] = val
