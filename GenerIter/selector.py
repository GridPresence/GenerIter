"""
Class to catalogue and select source files.

Copyright 2020 Thomas Jackson Park & Jeremy Pavier

"""
import os
import string
import random
import json
import GenerIter.excepts as robox
from GenerIter.source import WavSource
from GenerIter.config import Config
from GenerIter.util import jStr, debug, debug_except

class Selector():
    """Represents the inventory of samples available for algorithmic processing.
    
    .. code-block:: python
       :caption: Example constructor usage
       
       from GenerIter.selector import Selector
       # Selector
       selector = Selector(searchpath=pathstring,loadpath=loadfile)

    """
    
    def __init__(self, searchpath=None, loadpath=None):
        self._data = {}
        if searchpath is not None:
            self.search(spath=searchpath)
        if loadpath is not None:
            self.load(lpath=loadpath)

    def subcats(self):
        """Get the list of top-level sub-categories in the Selector.

        Returns:
            [] (str)
        .. code-block:: python
           :caption: Example usage
           
           # Enumerate the sub-categories
           cats = selector.subcats()
           for cat in cats:
               # Get the sub-category
               category = selector[cat]
        
        """
        retval = []
        for key in self._data:
            retval.append(key)
        return retval
        
    def __str__(self):
        return jStr(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def selectRandom(self, key):
        """Method for getting a random selection from within a sub-category of the Selector.

        This method will attempt to randomly choose an entry for the specified sub-category in the Selector.

        It will fail if there are no ``true`` enabled entries in the sub-category or if the randomised function repeatedly
        fails to find a ``true`` enabled entry because they are too sparse.

        The number of attempts is limited by the size of the sub-category array.

        Args:
            key (str) : the name of a sub-category within the Selector's structure.

        Raises:
            RDJParameterErr : if unable to select a return value.
        """
        retval = None
        if key is not None:
            # How many entries are there in this category?
            sellen = len(self._data[key])
            # Let's not try selecting on an empty set
            if sellen > 0:
                # If I can't select after that number of tries, there's a probably an issue
                ctr = sellen
                # Set a limit
                while ctr > 0:
                    src, incl = random.choice(list(self._data[key].items()))
                    if incl is True:
                        # We have a selection
                        retval = src
                        # Skip to the end.
                        ctr = 0
                    else:
                        # Marked as excluded
                        retval = None
                    # Need to avoid an infinite loop if ALL the entries got
                    # accidentally excluded.
                    ctr = ctr - 1
        # Houston, we have a problem
        if retval is None:
            raise robox.RDJParameterErr("Unable to select a valid source for {0}".format(key))
        # Here's a result.
        return retval

    def search(self, spath=None):
        """Walk a directory tree to add to the Selector configuration.

        This method walks the specified directory tree and adds any discovered WAV files to its inventory.
        This method is uniquely additive in that it can be run repeatedly across the different or the same trees.
        Uniqueness is enforced during this process, so any repeats are silently overwritten.
        Any files encountered that do not match the criteria for a WAV file are ignored.

        Args:
            spath (str) : path to the root of the searchble directory tree.

        .. code-block:: python
           :caption: Example usage
       
           from GenerIter.selector import Selector
           # Empty Selector
           selector = Selector()
           # Search a directory tree
           selector.search(spath=pathstring)


        """
        if spath is not None:
            #debug(spath)
            for subdir, dirs, fyles in os.walk(spath):
                #debug((subdir, dirs, fyles))
                for fyle in fyles:
                    #debug(fyle)
                    filepath = "{0}{1}{2}".format(subdir,
                                                  os.sep,
                                                  fyle)
                    #debug(filepath)
                    # Attempt to add this item into the current configuration
                    try:
                        # Is it a valid WavSource?
                        src = WavSource(dpath=filepath, dexist=True)
                    except Exception as inst:
                        debug(filepath)
                        #debug_except(inst)
                        debug("skipping ...")
                        src = None # The insert will skip this
                    self.insert(source=src, include=True)

    def load(self, lpath=None):
        """Load a previously-saved Selector configuration.

        This method is uniquely additive in that it can be run repeatedly and any repeats are silently overwritten.

        Args:
            lpath (str) : path to the loadable JSON file containing a saved Selector state.

        .. code-block:: python
           :caption: Example usage
       
           from GenerIter.selector import Selector
           # Empty Selector
           selector = Selector()
           # Load a previously-saved inventory file
           selector.load(lpath=pathstring)

        """
        if lpath is not None:
            # Open the specified JSON file and load it
            with open(lpath) as fp:
                #debug("Open {0}".format(lpath))
                tcand = json.load(fp)
            # Iterate down the categories
            for category in tcand:
                # Within each category, iterate down the items
                for item in tcand[category]:
                    # Attempt to add this item into the current configuration
                    try:
                        # Is it a valid WavSource?
                        src = WavSource(dpath=item, dexist=True)
                    except robox.RDJValidationErr as err:
                        debug(err)
                        debug("WavSource exception for {0}".format(item))
                        src = None # The insert will skip this
                    self.insert(source=src, include=tcand[category][item])

    def insert(self, source, include=True):
        """Attempt to insert a source into the Selector configuration
        """
        #debug(source)
        if source is not None:
            # Force case-insensitivity in the keys
            lower_key = source.dname.lower()
            # Capitalise the first letter
            key = string.capwords(lower_key)
            if key in self._data:
                # If this key already exists, that's fine
                pass
            else:
                # If the key doesn't exist, create the dictionary for its entries
                self._data[key] = {}
            # Insert the entry in the correct subcategory
            self._data[key][source.path] = include
            

    
