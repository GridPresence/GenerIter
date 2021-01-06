#!/usr/bin/env python3
"""
App to generate music.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import argparse

from GenerIter.app.clibase import CLIBase
from GenerIter.selector import Selector
from GenerIter.config import Config
from GenerIter.factory import ProcessorFactory
import GenerIter.excepts as gix
from GenerIter.util import debug, localTimestamp

class Generator(CLIBase):

    def _init_(self):
        super(CLIBase, self).__init__()


    def parseArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-I", help="Source for inclusion in searches",
                            action='append')
        parser.add_argument("-L", help="Source selection file for inclusion in loads",
                            action='append')
        parser.add_argument("-C", help="Configuration file for algorithms",
                            action='store', required=True)
        
        args = parser.parse_args()
        
        self._includes = args.I
        self._loads = args.L
        #self._outfile = "{0}.wav".format(args.o)
        self._confname = args.C

    def loadSelections(self):
        self._selector = Selector()
        if self._includes is not None:
            for srcdir in self._includes:
                self._selector.search(srcdir)
        if self._loads is not None:
            for load in self._loads:
                self._selector.load(load)

    def loadConfiguration(self):
        self._configuration = Config()
        self._configuration.load(self._confname)
        #debug(self._configuration)
        self._voices = self._configuration.subcats()
        #debug(self._voices)
        self._sequence = None
        self._destination = os.getcwd()
        self._format = "wav"
        try:
            if "sequence" in self._configuration["Globals"]:
                if len(self._configuration["Globals"]["sequence"]) > 0:
                    self._sequence = self._configuration["Globals"]["sequence"]
        except KeyError:
            pass

        try:
            if "destination" in self._configuration["Globals"]:
                self._destination = self._configuration["Globals"]["destination"]
        except KeyError:
            pass
        
        try:
            if "format" in self._configuration["Globals"]:
                self._format = self._configuration["Globals"]["format"]
        except KeyError:
            pass

        ts = localTimestamp()
        self._destination = os.path.join(self._destination, ts)
        #debug(self._destination)
        #debug(self._sequence)
        #debug(self._format)
                

    def process(self):
        self.loadSelections()
        self.loadConfiguration()
        if self._sequence is not None:
            for voice in self._sequence:
                debug(f"Voice : {voice}")
                for processor in self._configuration[voice]:
                    debug(f"Processor : {processor}")
                    factory = ProcessorFactory(voice, processor, self._configuration[voice][processor])
                    factory.configure(invent=self._selector,
                                      config=self._configuration[voice][processor],
                                      dest=self._destination,
                                      form=self._format)
                    factory.process()
        else:
            for voice in self._voices:
                if voice != "Globals":
                    for processor in self._configuration[voice]:
                        factory = ProcessorFactory(voice, processor, self._configuration[voice][processor])
                        factory.configure(invent=self._selector,
                                          config=self._configuration[voice][processor],
                                          dest=self._destination,
                                          form=self._format)
                        factory.process()

#if __name__ == '__main__':
#    app = Generator()
