import pytest
from pyrobodj.selector import Selector
import pyrobodj.excepts as robox
from pyrobodj.util import jStr, debug

LOADPATH = "./pyrobodj_test_data/inventory.json"
TSBCTS = ['Atmos',
          'Bass',
          'Brass',
          'Drums',
          'Effects',
          'Fx',
          'Guitar',
          'Keys',
          'Pads',
          'Percussion',
          'Strings',
          'Synth',
          'Vocals',
          'Voices',
          'Wind']

def test_loader():
    """Creates a simple Selector object from a load file"""
    test = Selector(loadpath=LOADPATH)
    # This is a bit noddy inasmuch as if you get here without throwing an unhandled exception
    # it's passed muster. A smoke test at best.

def test_subcats():
    test = Selector(loadpath=LOADPATH)
    test_sbcts = test.subcats()
    # Expect the two arrays to have same length
    assert(len(TSBCTS) == len(test_sbcts))
    # Expect each array to contain same entries as each other
    for entry in TSBCTS:
        assert(entry in test_sbcts)

def test_select_random():
    test = Selector(loadpath=LOADPATH)
    test_sbcts = test.subcats()
    test_sbcts_len = len(test_sbcts)
    # This is just a functional smoke test
    # since the outcomes should be random
    for ctr in range(test_sbcts_len):
        voice = test_sbcts[ctr]
        debug(voice)
        for ictr in range(5):
            selected = test.selectRandom(voice)
            debug("\t{0}".format(selected))
    
    
