"""
Generator class for all Process-based Bass algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug

class Beats(Process):
    def __init__(self):
        super(Beats, self).__init__()
        debug('Beats()')

    def algorithm01(self):
        """ This is a direct replication of the Beats algorithm in the original
        DJProcessor code."""
        # These could be parameterised in the config
        DECLICK = 10
        BEATS_VOL_RANGE = (14, 18)
        BASS_VOL_RANGE = (18, 22)
        DRONES_VOL_RANGE = (18, 22)
        
        # How many times do you want this to run?
        iterations = int(self._config["iterations"])
        # Need to be able to pad the correct number of zeroes
        digits = self.intwidth(iterations)
        # What's the base root name of the outputs?
        track = self._config["track"]
        # Where are we sending the outputs?
        dest = self._config["destination"]
        # Track repeats
        repeats = int(self._config["repeats"])

        for ctr in range(iterations):
            # Randomly select our samples
            beats_sample = self._inventory.selectRandom("Beats")
            bass_sample = self._inventory.selectRandom("Bass")
            drone_sample = self._inventory.selectRandom("Drones")

            # Instantiate the audio segment
            beats_audio = AudioSegment.from_wav(beats_sample)
            # Adjust amplitudes and fades
            beats_audio = self.deamplify(beats_audio, BEATS_VOL_RANGE)
            beats_audio = self.declick(beats_audio, DECLICK)
            
            bass_audio = AudioSegment.from_wav(bass_sample)
            bass_audio = self.deamplify(bass_audio, BASS_VOL_RANGE)
            bass_audio = self.declick(bass_audio, DECLICK)
            
            drones_audio = AudioSegment.from_wav(drones_sample)
            drones_audio = self.deamplify(drones_audio, DRONES_VOL_RANGE)
            drones_audio = self.declick(drones_audio, DECLICK)

            bb_overlay = beats_audio.overlay(bass_audio)
            composite_01 = bb_overlay + bb_overlay + bb_overlay + bb_overlay

            dbb_overlay = composite_01.overlay(drones_audio)

            for ctr2 in range(repeats):
                dbb_overlay = dbb_overlay + dbb_overlay
            # Create the output file name with zero padded counter value
            filename = "{0}_{1}.wav".format(track, str(ctr).zfill(digits))
            # Set up the output path
            dest = os.path.join(destination, filename)
            # Write it out
            dbb_overlay.export(dest, format="wav")

    def algorithm02(self):
        """ This is a variant of the algorithm01 in the original
        DJProcessor code."""
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
            drums_sample = self._inventory.selectRandom("Drums")
            bass_sample = self._inventory.selectRandom("Bass")
            pads_sample = self._inventory.selectRandom("Pads")

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
            # Create the output file name with zero padded counter value
            #if self.supported(self._config["format"]) is True:
            #   filename = "{0}_{1}.{2}".format(track, str(ctr).zfill(digits), self._config["format"])
            #  # Set up the output path
            # destination = os.path.join(dest, filename)
            # Write it out
            # dbb_overlay.export(destination, format=self._config["format"])
            import inspect

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=dbb_overlay)
            
            
