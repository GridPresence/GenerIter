"""
Abstract base class for all Process-based generator algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import math
import random
from pydub import AudioSegment
from GenerIter.selector import Selector
from GenerIter.source import WavSource
from GenerIter.util import debug, jStr, mkdir_p

class Process():
    # Currently only WAV is supported, but this list is expected to grow
    SUPPORTED_FORMATS = ["wav"]

    def __init__(self, prefix=None):
        self._config = None
        self._inventory = None
        self._destination = None
        self._format = "wav"
        self._content = []
        self._prefix = prefix
        debug('Process()')

    def configure(self, inventory, configuration, destination, forrmat):
        self._config = configuration
        self._inventory = inventory
        self._destination = destination
        self._format = forrmat

    def default(self):
        debug('No-op default processing logic')
        debug(type(self))

    def declick(self, segment, value):
        segment = segment.fade_in(value)
        segment = segment.fade_out(value)
        return segment

    def deamplify(self, segment, limits):
        diminish = random.randrange(limits[0], limits[1])
        segment = segment - diminish
        return segment

    def getsegment(self, sample, limits, fade):
        retval = AudioSegment.from_wav(sample)
        retval = self.deamplify(retval, limits)
        retval = self.declick(retval, fade)
        return retval

    def intwidth(self, value):
        retval = 1 + int(math.log10(value))
        return retval

    def supported(self, value):
        return value in self.SUPPORTED_FORMATS

    def write(self, algorithm, counter, source):
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Need to be able to pad the correct number of zeroes
        digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        base = type(self).__name__
        # Set the correct sub directory and ensure it exists
        destdir = os.path.join(self._destination, base)
        mkdir_p(destdir)
        # Zero pad the counter string
        ctr = str(counter).zfill(digits)
        track = f"{base}_{algorithm}_{ctr}"
        debug(f"Track: {track}")

        # Create the output file name with zero padded counter value
        if self.supported(self._format) is True:
            filename = "{0}.{1}".format(track, self._format)
            # Set up the output path
            dest = os.path.join(destdir, filename)
            print(f"\t{dest}")
            # Write it out
            source.export(dest, format=self._format)
            src = WavSource(dpath=dest, dexist=True)
            self._inventory.insert(src)
        else:
            print("Unsupported output format : {0}".format(self._format))
