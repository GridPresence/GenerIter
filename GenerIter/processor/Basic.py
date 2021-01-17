"""
Generator class for some fundamental Process-based algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug

class Basic(Process):
    def __init__(self):
        super(Basic, self).__init__()
        debug('Basic()')

    def beatsbassdrone(self):
        """ This is a variant of the algorithm01 in the original
        DJProcessor code.

        As the name suggests, it expects to find categories in the sample inventory mapped into the Beats, Bass and Drone voices. 
        Otherise this algorithm will fail."""
        # These could be parameterised in the config
        DECLICK = 10
        DRUMS_VOL_RANGE = (14, 18)
        BASS_VOL_RANGE = (18, 22)
        PADS_VOL_RANGE = (18, 22)
        
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Need to be able to pad the correct number of zeroes
        digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        #track = self._config["track"]
        # Where are we sending the outputs?
        dest = self._destination
        # Track repeats
        repeats = int(self._config["repeats"])

        for ctr in range(iterations):
            # Randomly select our samples
            drums_sample = self._inventory.selectRandom("Beats")
            bass_sample = self._inventory.selectRandom("Bass")
            pads_sample = self._inventory.selectRandom("Drone")

            # Instantiate the audio segment
            drums_audio = AudioSegment.from_wav(drums_sample)
            # Adjust amplitudes and fades
            drums_audio = self.deamplify(drums_audio, DRUMS_VOL_RANGE)
            drums_audio = self.declick(drums_audio, DECLICK)
            
            bass_audio = AudioSegment.from_wav(bass_sample)
            bass_audio = self.deamplify(bass_audio, BASS_VOL_RANGE)
            bass_audio = self.declick(bass_audio, DECLICK)
            
            pads_audio = AudioSegment.from_wav(pads_sample)
            pads_audio = self.deamplify(pads_audio, PADS_VOL_RANGE)
            pads_audio = self.declick(pads_audio, DECLICK)

            bb_overlay = drums_audio.overlay(bass_audio)
            composite_01 = bb_overlay + bb_overlay + bb_overlay + bb_overlay

            dbb_overlay = composite_01.overlay(pads_audio)

            for ctr2 in range(repeats):
                dbb_overlay = dbb_overlay + dbb_overlay
            
            import inspect

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=dbb_overlay)


    def voices3(self):
        """ This algorithm uses the same algorith as beatsbassdrone, 
        but allows the user to designate the 3 voices to be used in the compose file."""
        # These could be parameterised in the config
        DECLICK = 10
        DRUMS_VOL_RANGE = (14, 18)
        BASS_VOL_RANGE = (18, 22)
        PADS_VOL_RANGE = (18, 22)
        
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        # Need to be able to pad the correct number of zeroes
        digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        #track = self._config["track"]
        # Where are we sending the outputs?
        dest = self._destination
        # Track repeats
        repeats = int(self._config["repeats"])

        voices = self._config["voices"]

        for ctr in range(iterations):
            # Randomly select our samples
            drums_sample = self._inventory.selectRandom(voices[0])
            bass_sample = self._inventory.selectRandom(voices[1])
            pads_sample = self._inventory.selectRandom(voices[2])

            # Instantiate the audio segment
            drums_audio = AudioSegment.from_wav(drums_sample)
            # Adjust amplitudes and fades
            drums_audio = self.deamplify(drums_audio, DRUMS_VOL_RANGE)
            drums_audio = self.declick(drums_audio, DECLICK)
            
            bass_audio = AudioSegment.from_wav(bass_sample)
            bass_audio = self.deamplify(bass_audio, BASS_VOL_RANGE)
            bass_audio = self.declick(bass_audio, DECLICK)
            
            pads_audio = AudioSegment.from_wav(pads_sample)
            pads_audio = self.deamplify(pads_audio, PADS_VOL_RANGE)
            pads_audio = self.declick(pads_audio, DECLICK)

            bb_overlay = drums_audio.overlay(bass_audio)
            composite_01 = bb_overlay + bb_overlay + bb_overlay + bb_overlay

            dbb_overlay = composite_01.overlay(pads_audio)

            for ctr2 in range(repeats):
                dbb_overlay = dbb_overlay + dbb_overlay
            
            import inspect

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=dbb_overlay)
            
            
