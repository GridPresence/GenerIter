"""
Classes to represent references to GenerIter source files.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import GenerIter.excepts as robox
from GenerIter.util import jStr, debug

class Source():
    """Generic file source representation.

    Args:
        path (string) : string representation of the absolute or relative path to the target file.
        exist (boolean) : flag setting to test for the file's existence when the reference object is instantiated.

    Raises:
        GIResourceErr : if ``exist == True`` and the file does not exist.
    """
    def __init__(self, path=None, exist=False):
        """Init docstring
        """
        self._path = None
        self._fname = None
        self._root = None
        self._ext = None
        
        self.path = path
        if exist is True:
            if self.exists() is not True:
                raise robox.GIResourceErr("File {0} does not exist.".format(self.path))

    @property
    def path(self):
        """Accessor to the  value of full path value
        """
        return self._path

    @path.setter
    def path(self, value):
        """Sets value of full path.
 
        Also derives various component features from the path
        """
        if value is None:
            raise robox.GIParameterErr("No path given on Source class path setting accessor.")
        self._path = value
        self._fname = os.path.basename(self._path)
        self._dname = os.path.basename(os.path.dirname(self._path))
        self._root, self._ext = os.path.splitext(self._fname)

    @property
    def root(self):
        """Returns the root name of the file.
        """
        return self._root

    @property
    def fname(self):
        """Returns the basename of the file.
        """
        return self._fname

    @property
    def dname(self):
        """Returns the name of the file's directory.
        """
        return self._dname

    @property
    def ext(self):
        """Returns the filename extension of the file
        """
        return self._ext

    def isValidExtension(self, ref=None):
        """Tests if the filename extension matches an expected value.

        Indicates whether the Source or derived object carries the same file extension, either as upper- or lower-case forms.

        Args:
            ref (str) : the extension value to compare against.

        Returns:
            boolean
        """
        if ref is None:
            # This is essentially a NOOP
            return True
        else:
            if self.ext is None:
                return False
            case1 = (ref == self.ext.upper())
            case2 = (ref == self.ext.lower())
            return (case1 | case2)

    def exists(self):
        """Test if the file referred to exists.

        Returns:
            boolean
        """
        return os.path.isfile(self.path)

    def __str__(self):
        """Returns a string representation of the object variables.
        """
        return jStr(vars(self))

class WavSource(Source):
    """Derived class specialised for WAV source files.
    """
    def __init__(self, dpath=None, dexist=False):
        """Instantiates as a Source file then validates the filename extension.
        """
        super(WavSource, self).__init__(path=dpath, exist=dexist)
        if self.isValidExtension('.wav') is not True:
            raise robox.GIValidationErr("Incorrect file extension for WavSource.")

class FlacSource(Source):
    """Derived class specialised for FLAC source files.
    """
    def __init__(self, dpath=None, dexist=False):
        """Instantiates as a Source file then validates the filename extension.
        """
        super(FlacSource, self).__init__(path=dpath, exist=dexist)
        if self.isValidExtension('.flac') is not True:
            raise robox.GIValidationErr("Incorrect file extension for FlacSource.")

class Mp3Source(Source):
    """Derived class specialised for MP3 source files.
    """
    def __init__(self, dpath=None, dexist=False):
        """Instantiates as a Source file then validates the filename extension.
        """
        super(Mp3Source, self).__init__(path=dpath, exist=dexist)
        if self.isValidExtension('.mp3') is not True:
            raise robox.GIValidationErr("Incorrect file extension for Mp3Source.")
        
