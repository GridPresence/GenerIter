"""
Useful unencapsulated functions to be reused across the domain.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
from __future__ import print_function

import os
import errno
import json
from datetime import datetime, date
from subprocess import check_output, CalledProcessError

def debug(astring):
    """Only print if in DEBUG mode.

    Args:
        astring(str) : any valid Python string
    """
    if __debug__:
        print(astring)

def debug_except(inst):
    """Only print exception diagnostics if in DEBUG mode.

    Args:
        inst : any valid exception instance
    """
    if __debug__:
        print(type(inst))
        print(inst.args)
        print(inst)

def jsonSerial(obj):
    """JSON serializer for objects not serializable by default json code.

    Currently supports datetime objects.

    Args:
        obj (any type) : arbitary Python object or type.

    Returns:
        string

    Raises:
        TypeError : if the object is not serializable.
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {0} not serializable".format(type(obj)))

def jStr(struct):
    """Default JSON output human-readable string format.

    The output string is formatted for ease of reading, with an indent value of 4 chars,
    using standard separators and all fields sorted by name at their appropriate level.

    Args:
        struct : arbitary Python iterable data structure i.e. list or dict.

    Returns:
        string
    """
    if struct is None:
        struct = {}
    return json.dumps(struct,
                      default=jsonSerial,
                      sort_keys=True,
                      indent=4,
                      separators=(",", ":"))

def shCmd(cspec, trace=False):
    """Executes a shell command and returns a string list of the output.

    Args:
        cspec [] : array of command line options and parameters.
        trace (boolean) : flag to set for text output if required (default : False)

    Returns:
        [] (str) if ``trace == True`` else ``None``

    Raises:
        CalledProcessError : if the subprocess call fails
    """
    debug("Executing: {0}".format(cspec))
    retval = None
    try:
        intermed = check_output(cspec).decode("utf-8").rstrip()
        retval = intermed.split("\n")
        if trace is True:
            for line in retval:
                print(line)
    except CalledProcessError:
        retval = None
    return retval

def utf8(array):
    """Preserves byte strings, converts Unicode into UTF-8.

    Args:
        array (bytearray or str) : input array of bytes or chars

    Returns:
        UTF-8 encoded bytearray
    """
    retval = None
    if isinstance(array, bytes) is True:
        # No need to convert in this case
        retval = array
    else:
        retval = array.encode("utf-8")
    return retval


def mkdir_p(path):
    """Replicates mkdir -p functionality.

    For a given path, any missing directories are created to ensure the full path exists

    Args:
        path (str): absolute path to the target directory.

    Raises:
        OSError : if the path already exists as a file, or the target directory cannot be created because of a permissions error.
    """
    try:
        # Try to make all the necessary missing directories in the given path
        os.makedirs(path)
    except OSError as exc:
        # If the directory already exists on this path, that's okay
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # Otherwise, it's either just a file or there's a permissions problem
        else:
            raise

def localTimestamp(some_time=None, time_format=None):
    """Return a specified UTC time, formatted by the given string.

    Args:
        some_time: a datetime object (default ``None`` uses ``datetime.utcnow()``)
        time_format: format to covert a datetime object to string (default ``None`` uses ``%Y%m%d%H%M%S``)

    Returns:
        A timestamp string
    """
    TIME_FORMAT_STRING = "%Y_%m%b_%dT%H_%M_%S_%fUTC"
    COMPACT_TIME_FMT = "%Y%m%d%H%M%S"
    if some_time is None:
        the_time = datetime.utcnow()
    else:
        the_time = some_time
    if time_format is None:
        the_time_format = COMPACT_TIME_FMT
    else:
        the_time_format = time_format
    time_string = the_time.strftime(the_time_format)
    return time_string
