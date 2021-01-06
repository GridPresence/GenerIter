import pytest
import json
from pyrobodj.config import Config
import pyrobodj.excepts as robox
from pyrobodj.util import jStr, debug

CPATH = "pyrobodj_test_data/test_conf.json"

def test_simple_constructor():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config()
    debug(test01)

def test_simple_load_constructor():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config(confpath=CPATH)
    debug(test01)

def test_simple_load_01():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config()
    test01.load(inpath=CPATH)
    debug(test01)

def test_subcats():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config(confpath=CPATH)
    test02 = test01.subcats()
    debug(test02)

def test_getitem():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config(confpath=CPATH)
    test02 = test01.subcats()
    for item in test02:
        test03 = test01[item]
        debug('{0} - {1}'.format(item, test03))

def test_setitem():
    """
    Creates a reference for a non-existent file, but does not test for existence.
    """
    test01 = Config(confpath=CPATH)
    test02 = test01.subcats()
    for item in test02:
        test03 = test01[item]
        test03['NewVar'] = 'NewVal'
        test03['NewVar02'] = 12345
    debug(test01)


