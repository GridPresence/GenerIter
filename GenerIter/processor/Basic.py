"""
Generator class for some basic Process-based algorithms for rhythmic generation.
"""
import os
import random
import inspect
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug, nextPowerOf2
import GenerIter.excepts as robox

class Basic(Process):
    def __init__(self):
        super().__init__()
        debug('Basic()')

    def beatsbassdrone(self):
        """ This is a developmental prototype variant of the algorithm01 in the original
        DJProcessor code.

        As the name suggests, it expects to find categories in the sample inventory mapped into the *Beats*, *Bass* and *Drone* voices. 
        Otherise this algorithm will fail.
        
        Warning:
            This is example code used during early development, and should really only be used for reference and study.

        """
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
        """ This developmental prototype algorithm uses the same algorithm as beatsbassdrone, 
        but allows the user to designate the 3 voices to be used in the compose file.

        The number of voices allowed is hard-coded to 3 only.

        
        Warning:
            This is example code used during early development, and should really only be used for reference and study.

        """
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
            # Set a soft threshold for the size of the piece
            size_limit = self.threshold()
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
        """ This developmental prototype algorithm uses the same algorithm as voices3, 
        but allows the user to designate the 3 or more voices to be used in the compose file.

        Warning:
            This is example code used during early development, and should really only be used for reference and study.

        """
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
        """ This algorithm uses the same algorithm as voices, 
        but implements a sequential shift as each new voice is incorporated.

        Warning:
            This is example code used during early development, and should really only be used for reference and study.
        """
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


    def groove(self):
        """The `Basic.groove` algorithm is used to form a rhythmic backbone to a composition. This algorithm attempts to make sensible alignment
        choices for the samples in use. It is considered a *production* algorithm.

        .. image:: images/Basic.groove.jpg

        The number of voices can be 3 or more. In this example we are using 4, which we can think of as **A**, **B**, **C** and **D** corresponding
        to their declaration position in the configuration list.

        Segments **A** and **B** are randomly selected from their inventory categories. These are then length-aligned. That is, whichever is the
        shorter of the two is padded with exactly the right amount of silence to make the frame lengths of both segments equal. These are then overlayed
        to form a composite rhythmic unit referred to as **AB**.

        The basic rhythmic beat is created by replicating a sequence of these **AB** segments end-to-end until the track size limit is surpassed.
        This is the `groove_base`.

        The `cycle` parameter specifies the number of these **AB** components tahe represent a higher level repetition unit called the `cycle` (obviously).

        Subsequent voices are also length-aligned (or curtailed) to match the size of the **AB** unit. A new segment, `groove_layer` is created,
        into which the later voices **C**, **D**, etc. are injected in a cyclic sequence, aligned precisely to the `groove_base` cycles and beats.

        Finally, the `groove_base` is overlayed with the `groove_layer` to create a composite whole track which is output as an audio file.

        Parameters:
            tracks (int) : number of times the process is to run.
            voices (list) : list of voice categories to select and use in the track
            cycle (int) : length of a repeat cycle in terms of groove_base *beats*

        Example:

        .. code:: json

           {
               "Basic" : {
                   "groove" : {
                       "tracks" : 50,
                       "cycle" : 4,
                       "voices" : [
                           "Bass",
                           "Beat",
                           "Percussion",
                           "Pad"
                       ]
                    }
                }
            }

        Raises:
            GenerIter.excepts.GIParameterErr
        """
        declick = 10
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        voices = self._config["voices"]
        nvoices = len(voices)
        cycle = self._config["cycle"]
      
        if nvoices < 3:
            raise robox.GIParameterErr("Insufficient voices specified for the groove algorithm")

        # Need to keep all overlays below the clipping threshold
        mute = 6.0 * nextPowerOf2(nvoices)

        for ctr in range(iterations):
            audios = []
            maxlen = 0
            # Set a soft threshold for the size of the piece
            size_limit = self.threshold()
            # Randomly select our samples
            for voice in voices:
                sample = self._inventory.selectRandom(voice)
                audio = self.getsegmentm(sample, mute, declick)
                audios.append(audio)

            for aud in range(2):
                if len(audios[aud]) > maxlen:
                    maxlen = len(audios[aud])
                    
            for aud in range(2, nvoices):
                audios[aud] = self.padtolength(audios[aud], maxlen, declick)

            # Create the groove's rhythmic base layer
            rhythm = audios[0].overlay(audios[1])
            rlen = len(rhythm)
            groove_base = rhythm
            print("{0}  < {1}".format(str(groove_base.duration_seconds), str(size_limit)))
            while groove_base.duration_seconds < size_limit:
                #groove_base = groove_base + rhythm
                groove_base = groove_base + rhythm

            # Create a blank segment of same size and frame rate
            groove_layer = AudioSegment.silent(duration=len(groove_base),
                                               frame_rate=groove_base.frame_rate)

            for ctr2 in range(2, nvoices):
                compound = AudioSegment.silent(duration=cycle*len(rhythm),
                                               frame_rate=groove_layer.frame_rate)
                offset = ((ctr2 - 2) % cycle) * rlen
                compound = compound.overlay(audios[ctr2], position=offset)
                groove_layer = groove_layer.overlay(compound, loop=True)

            summation = groove_base.overlay(groove_layer)

            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=summation)
