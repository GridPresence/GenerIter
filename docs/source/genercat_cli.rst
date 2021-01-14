genercat
--------

.. code-block:: bash
		
   usage: genercat [-h] -C C [-D D]
   
   optional arguments:
       -h, --help  show this help message and exit
       -C C        Category search pattern
       -D D        Destination category name

The **genercat** console application is a helper utility for managing sample libraries. It can be used when you have a large, flat directory full of sample files and wish to apply some structure on the collection. This is particularly useful when you wish to create different voices or subcategories in you inventory (see below). You can use the app to assign sets of samples into a named subdirectory.

So, for example, if you wished to assign all your **Piano**-related content into a **Piano** subdirectory:

.. code-block:: bash

   genercat -C Piano

will create a `Piano` subdirectory (unless it already exists) in the current directory, and then move all the sample files whose name contains the string "Piano" into that subdirectory.

A more flexible use case is where you may want to organise different sample file types under a common category. One example would be a directory that contains a range of samples relating to different percussive sounds which you wanted to group together:

.. code-block:: bash

   genercat -D Percussion -C Drum
   genercat -D Percussion -C Hi-Hat
   genercat -D Percussion -C Snare
   genercat -D Percussion -C Topper
   genercat -D Percussion -C Riser

This takes all the files that match to patterns defined by the **-C** specifier and puts them in a common destination subdirectory as defined by the **-D** specifier.

The rule is that if only **-C** is specified, the destination subdirectory mirrors that selection. Otherwise, the files are moved into the subdirectory specified by **-D**.

This means that:

.. code-block:: bash

   genercat -C Drum
   genercat -D Drum -C Drum

are functionally identical.
