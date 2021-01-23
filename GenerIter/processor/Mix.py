"""
Generator class for some Process-based mixing algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
import inspect
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug, nextPowerOf2
import GenerIter.excepts as robox

class Mix(Process):
    def __init__(self):
        super().__init__()
        debug('Mix()')

    def multitrack(self):
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        voices = self._config["voices"]
        nvoices = len(voices)

        if nvoices < 2:
            raise robox.GIParameterErr("Insufficient voices specified for the multitrack algorithm")

        mute = 1.5 * nextPowerOf2(nvoices)

        for ctr in range(iterations):
            audios = []
            # Randomly select our samples
            for voice in voices:
                sample = self._inventory.selectRandom(voice)
                audio = AudioSegment.from_wav(sample)
                audio = audio.normalize()
                audio = audio - mute
                audios.append(audio)

            summation = audios[0]
            for nctr in range(nvoices-1):
                summation = summation.overlay(audios[nctr+1], loop=true)
            summation = summation.normalize()
            
            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=summation)
