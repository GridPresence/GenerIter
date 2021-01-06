import pytest
from pyrobodj.source import Source, WavSource
import pyrobodj.excepts as robox
from pyrobodj.util import jStr, debug
from pyrobodj.processor.Bass import Bass
from pyrobodj.processor.Brass import Brass
from pyrobodj.processor.Drums import Drums
from pyrobodj.processor.Guitars import Guitars
from pyrobodj.processor.Keys import Keys
from pyrobodj.processor.Vocals import Vocals

def test_brass_constructor():
    test01 = Brass()

def test_many_constructors():
    test_bass = Bass()
    test_brass = Brass()
    test_drums = Drums()
    test_guitars = Guitars()
    test_keys = Keys()
    test_vocals = Vocals()

def test_many_defaults():
    test_bass = Bass()
    test_bass.default()
    test_brass = Brass()
    test_brass.default()
    test_drums = Drums()
    test_drums.default()
    test_guitars = Guitars()
    test_guitars.default()
    test_keys = Keys()
    test_keys.default()
    test_vocals = Vocals()
    test_vocals.default()
