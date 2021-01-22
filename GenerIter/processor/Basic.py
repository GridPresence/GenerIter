"""
Generator class for some fundamental Process-based algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
import inspect
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug
import GenerIter.excepts as robox

class Basic(Process):
    def __init__(self):
        super().__init__()
        debug('Basic()')

    def beatsbassdrone(self):
        """ This is a variant of the algorithm01 in the original
        DJProcessor code.

        As the name suggests, it expects to find categories in the sample inventory mapped into the Beats, Bass and Drone voices. 
        Otherise this algorithm will fail."""
        # These could be parameterised in the config
        declick = 10
        drums_vol_range = (14, 18)
        bass_vol_range = (18, 22)
        pads_vol_range = (18, 22)
        
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Need to be able to pad the correct number of zeroes
        #digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        #track = self._config["track"]
        # Where are we sending the outputs?
        #dest = self._destination
        # Track repeats
        repeats = int(self._config["repeats"])

        for ctr in range(iterations):
            # Randomly select our samples
            drums_sample = self._inventory.selectRandom("Beats")
            bass_sample = self._inventory.selectRandom("Bass")
            pads_sample = self._inventory.selectRandom("Drone")

            # Instantiate the audio segments
            drums_audio = self.getsegment(drums_sample, drums_vol_range, declick)
            bass_audio = self.getsegment(bass_sample, bass_vol_range, declick)
            pads_audio = self.getsegment(pads_sample, pads_vol_range, declick)

            bb_overlay = drums_audio.overlay(bass_audio)
            composite_01 = bb_overlay + bb_overlay + bb_overlay + bb_overlay

            dbb_overlay = composite_01.overlay(pads_audio)

            for ctr2 in range(repeats):
                dbb_overlay = dbb_overlay + dbb_overlay

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=dbb_overlay)


    def voices3(self):
        """ This algorithm uses the same algorith as beatsbassdrone, 
        but allows the user to designate the 3 voices to be used in the compose file."""
        # These could be parameterised in the config
        declick = 10
        aa_vol_range = (14, 18)
        ba_vol_range = (18, 22)
        ca_vol_range = (18, 22)

        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Need to be able to pad the correct number of zeroes
        #digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        #track = self._config["track"]
        # Where are we sending the outputs?
        #dest = self._destination
        # Track repeats
        repeats = int(self._config["repeats"])

        voices = self._config["voices"]

        for ctr in range(iterations):
            # Randomly select our samples
            aa_sample = self._inventory.selectRandom(voices[0])
            ba_sample = self._inventory.selectRandom(voices[1])
            ca_sample = self._inventory.selectRandom(voices[2])

            # Instantiate the audio segments
            aa_audio = self.getsegment(aa_sample, aa_vol_range, declick)
            ba_audio = self.getsegment(ba_sample, ba_vol_range, declick)
            ca_audio = self.getsegment(ca_sample, ca_vol_range, declick)

            bb_overlay = aa_audio.overlay(ba_audio)
            composite_01 = bb_overlay + bb_overlay + bb_overlay + bb_overlay

            dbb_overlay = composite_01.overlay(ca_audio)

            for ctr2 in range(repeats):
                dbb_overlay = dbb_overlay + dbb_overlay

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=dbb_overlay)

    def voices(self):
        """ This algorithm uses the same algorith as voices3, 
        but allows the user to designate the 3 or more voices to be used in the compose file."""
        # These could be parameterised in the config
        declick = 10
        vol_range = (14, 22)

        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Track repeats
        repeats = int(self._config["repeats"])

        voices = self._config["voices"]
        nvoices = len(voices)
        if nvoices < 3:
            raise robox.GIParameterErr("Insufficient voices specified for the 'voices' algorithm")
        
        for ctr in range(iterations):
            audios = []
            # Randomly select our samples
            for voice in voices:
                sample = self._inventory.selectRandom(voice)
                audio = self.getsegment(sample, vol_range, declick)
                audios.append(audio)

            summation = audios[0]
            for nctr in range(nvoices-2):
                summation = summation.overlay(audios[nctr+1])

            composite = summation + summation + summation + summation

            final_overlay = composite.overlay(audios[nvoices-1])

            for ctr2 in range(repeats):
                final_overlay = final_overlay + final_overlay

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=final_overlay)

    def voices_shifted(self):
        """ This algorithm uses the same algorith as voices3, 
        but allows the user to designate the 3 or more voices to be used in the compose file."""
        # These could be parameterised in the config
        declick = 10
        vol_range = (14, 22)

        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Track repeats
        repeats = int(self._config["repeats"])

        voices = self._config["voices"]
        nvoices = len(voices)
        if nvoices < 3:
            raise robox.GIParameterErr("Insufficient voices specified for the 'voices' algorithm")

        for ctr in range(iterations):
            audios = []
            # Randomly select our samples
            for voice in voices:
                sample = self._inventory.selectRandom(voice)
                audio = self.getsegment(sample, vol_range, declick)
                audios.append(audio)

            summation = audios[0]
            for nctr in range(nvoices-1):
                summation = summation.overlay(audios[nctr+1])
                summation = summation + summation

            for ctr2 in range(repeats):
                summation = summation + summation

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=summation)
