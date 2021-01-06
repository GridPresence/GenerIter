import pytest
from pyrobodj.source import Source, WavSource
import pyrobodj.excepts as robox
from pyrobodj.util import jStr, debug
from pyrobodj.factory import ProcessorFactory

def test_factory_brass_constructor():
    test01 = ProcessorFactory(name='Brass', fname='default')
    execute = test01.method
    execute()

def test_factory_bass_constructor():
    test01 = ProcessorFactory(name='Bass', fname='default')
    execute = test01.method
    execute()

def test_factory_drums_constructor():
    test01 = ProcessorFactory(name='Drums', fname='default')
    execute = test01.method
    execute()

def test_factory_guitars_constructor():
    test01 = ProcessorFactory(name='Guitars', fname='default')
    execute = test01.method
    execute()

def test_factory_keys_constructor():
    test01 = ProcessorFactory(name='Keys', fname='default')
    execute = test01.method
    execute()

def test_factory_vocals_constructor():
    test01 = ProcessorFactory(name='Vocals', fname='default')
    execute = test01.method
    execute()


