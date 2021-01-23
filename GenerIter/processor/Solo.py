"""
Generator class for some Process-based soloing algorithms.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import random
import inspect
from pydub import AudioSegment
from GenerIter.process import Process
from GenerIter.util import debug
import GenerIter.excepts as robox


class Solo(Process):
    
    SOLOMAP = [
        {
            "upper" : 10000,
            "variation" : (800, 2400),
            "fades" : 100,
            "back_silence" : 4000
        },
        {
            "upper" : 60000,
            "variation" : (8000, 24000),
            "fades" : 3000,
            "front_silence" : 20000,
            "back_silence" : 40000
        },
        {
            "upper" : 60000,
            "variation" : (20000, 36000),
            "fades" : 3000,
            "front_silence" : 60000,
            "back_silence" : 40000
        },
        {
            "upper" : 10000,
            "variation" : (200, 800),
            "fades" : 10,
            "front_silence" : 60000,
            "back_silence" : 40000,
            "reps" : (5, 30)
        }
    ]
    
    def __init__(self):
        super().__init__()
        debug('Solo()')

    def generic(self):
        VOL_UP = 14
        VOL_DN = 18
        # How many times do you want this to run?
        iterations = int(self._config["tracks"])
        
        voice = self._config["voice"]

        for ctr in range(iterations):
            # Grab some source material
            sample = self._inventory.selectRandom(voice)
            newAudio = AudioSegment.from_wav(sample)
            alen = len(newAudio)

            # Randomly select the parameters
            params = random.choice(self.SOLOMAP)

            # Are we trimming the input sample?
            if alen > params["upper"]:
                # Pick a random length
                samplen = random.randrange(params["variation"][0], params["variation"][1])
                # Define the range in which we can start the cut
                sampst = alen - samplen
                # Generate a start cut point in the defined range
                t1 = random.randrange(sampst)
                # Derive the endpoint of the cut
                t2 = (t1 + samplen)
                # Cut
                newAudio = newAudio[t1:t2]
                
            # Set a volume
            newvol = random.randrange(VOL_UP, VOL_DN)
            newAudio = newAudio - newvol

            # Set fades as defined by the params
            newAudio = self.declick(newAudio, params["fades"])

            # Do we need to pad front and/or back with some silence?
            if "front_silence" in params:
                if "back_silence" in params:
                    fsil = random.randrange(params["front_silence"])
                    bsil = random.randrange(params["back_silence"])
                    front = AudioSegment.silent(duration=fsil)
                    back = AudioSegment.silent(duration=bsil)
                    newAudio = front + newAudio + back
                else:
                    fsil = random.randrange(params["front_silence"])
                    front = AudioSegment.silent(duration=fsil)
                    newAudio = front + newAudio
            else:
                if "back_silence" in params:
                    bsil = random.randrange(params["back_silence"])
                    back = AudioSegment.silent(duration=bsil)
                    newAudio = newAudio + back
            
            # Do we wish to build repeats of this sample?
            if "reps" in params:
                addAudio = newAudio
                reps = random.randrange(params["reps"][0], params["reps"][1])
                for sam in range(reps):
                    newAudio += addAudio

            # Randomise front and back padding on the whole shebang
            dic = random.randrange(10)
            if dic == 7:
                sil1 = random.randrange(90000)
                sil2 = random.randrange(90000)
                solofront = AudioSegment.silent(duration = sil1)
                soloback = AudioSegment.silent(duration = sil2)
                newAudio = solofront + newAudio + soloback

            # Write it out
            fname = inspect.currentframe().f_code.co_name
            self.write(algorithm=fname, counter=ctr, source=newAudio)
