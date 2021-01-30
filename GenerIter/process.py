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
    """This is the abstract base class from which all other processors are derived.

    As such it implements the core interface as well as several important generic helper services which can simplify the derived algorithm implementations.
    """
    # Currently only WAV is supported, but this list is expected to grow
    SUPPORTED_FORMATS = ["wav"]

    TSHIRT = {
        "s" : 180,
        "m" : 300,
        "l" : 480,
        "xl" : 780,
        "xxl" : 1260,
        "xxxl" : 2640
    }

    def __init__(self, prefix=None):
        self._config = None
        self._inventory = None
        self._destination = None
        self._format = "wav"
        self._content = []
        self._prefix = prefix
        self._tsize = "m"
        debug('Process()')

    def configure(self, inventory, configuration, destination, forrmat, tsize):
        self._config = configuration
        self._inventory = inventory
        self._destination = destination
        self._format = forrmat
        self._tsize = tsize

    def default(self):
        debug('No-op default processing logic')
        debug(type(self))

    def declick(self, segment, value):
        """This is a helper function with which a sharp fade/rise can be applied to each end of an AudioSegment to reduce the potential for 
        'clicking' when they are connected end-to-end.
        Args:
            value (int) : number of frames across which the sample will be faded from full gain to zero (typically 10 seems to work well).

        Returns:
            AudioSegment
        """
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

    def getnormedsegment(self, sample, muted, fade):
        retval = AudioSegment.from_wav(sample)
        retval = retval.normalize()
        if muted > 0:
            reteval = retval - muted
        if fade > 0:
            retval = self.declick(retval, fade)
        return retval


    def intwidth(self, value):
        retval = 1 + int(math.log10(value))
        return retval

    def supported(self, value):
        return value in self.SUPPORTED_FORMATS

    def threshold(self):
        if self._tsize in self.TSHIRT:
            target = self.TSHIRT[self._tsize]
        else:
            target = self.TSHIRT["m"]
        lbnd = (9 * target) // 10
        ubnd = (11 * target) // 10
        retval = random.randrange(lbnd, ubnd)
        return retval

    def padtolength(self, segment, length, fader, front=False):
        quiet = length - len(segment)
        if quiet <= 0:
            retval = segment[:length]
            retval = self.declick(retval, fader)
        else:
            pad = AudioSegment.silent(duration=quiet,
                                      frame_rate=segment.frame_rate)
            if front is False:
                retval = segment + pad
            else:
                retval = pad + segment
        return retval

    def bracket(self, segment, frontmult=1.0, backmult=1.0):
        frunt = random.randrange(int(frontmult * len(segment)))
        bak = random.randrange(int(backmult * len(segment)))
        front = AudioSegment.silent(duration=frunt, frame_rate=segment.frame_rate)
        back = AudioSegment.silent(duration=bak, frame_rate=segment.frame_rate)
        retval = front + segment + back
        return retval
        
        

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
