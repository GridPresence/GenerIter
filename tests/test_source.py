import pytest
from pyrobodj.source import Source, WavSource
import pyrobodj.excepts as robox
from pyrobodj.util import jStr, debug

def test_simple_source_constructor():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    TESTPATH = "/usr/local/share/testfile.mp3"
    test01 = Source(path=TESTPATH)
    debug(test01)
    assert(test01.path == TESTPATH)
    assert(test01.fname == "testfile.mp3")
    assert(test01.root == "testfile")
    assert(test01.ext == ".mp3")
    assert(test01.isValidExtension(".mp3") is True)

def test_simple_source_constructor_exception():
    """ 
    Creates a reference for a non-existent file, tests for the existence of a non-existent
    file and throws an exception.
    """
    TESTPATH = "/usr/local/share/testfile.mp3"
    with pytest.raises(robox.RDJResourceErr):
        test01 = Source(path=TESTPATH, exist=True)

def test_empty_source_constructor_exception():
    """ 
    Creates a null reference for a file and throws an exception
    """
    with pytest.raises(robox.RDJParameterErr):
        test01 = Source()


def test_wav_source_constructor_exception():
    """ 
    Creates a Wav reference for a non-Wav file and throws an exception
    """
    TESTPATH = "/usr/local/share/testfile.mp3"
    with pytest.raises(robox.RDJValidationErr):
        test01 = WavSource(dpath=TESTPATH)
    
def test_simple_wav_source_constructor_exception():
    """ 
    Creates a reference for a non-existent WAV file, tests for the existence of a non-existent
    file and throws an exception.
    """
    TESTPATH = "/usr/local/share/testfile.wav"
    with pytest.raises(robox.RDJResourceErr):
        test01 = WavSource(dpath=TESTPATH, dexist=True)

def test_simple_wav_source_constructor():
    """
    Creates a reference for a non-existent Wav file, but does not test for existence.
    """
    TESTPATH = "/usr/local/share/testfile.wav"
    test01 = WavSource(dpath=TESTPATH)
    debug(test01)
    assert(test01.path == TESTPATH)
    assert(test01.fname == "testfile.wav")
    assert(test01.root == "testfile")
    assert(test01.ext == ".wav")
    assert(test01.isValidExtension(".wav") is True)
