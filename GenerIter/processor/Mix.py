"""
Generator class for some Process-based mixing algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
import inspect
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug
import GenerIter.excepts as robox

class Mix(Process):
    def __init__(self):
        super().__init__()
        debug('Mix()')
