Basic Workflow
--------------

The core **GenerIter** process is illustrated in the diagram:

.. image:: images/generiter-workflow.png
   :alt: GenerIter workflow


The basic workflow breaks down into 4 phases:

    #. Categorising the sample library
    #. Creating the sample inventory
    #. Creating the composer control file
    #. Generating music

Categorising the sample library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This first phase assumes the composer starts with an unstructured set of samples in one or more directories. To make the most out of the inventory classification system, it helps if the samples are organised in subdirectories named after the categories the composer finds useful. These category names can be clompletely arbitrary, but for this illustration I am going to use musical voice/instrument category specifiers like "Drums", "Bass", "Synths", etc.

The good news is that these categories can be specified at any level in your sample tree and don't require the "Drums" samples, for example to all be in a single directory.

The genercat_ utility is a helper command that allows the composer to allocate sets of sample files into named subdirectories, where the names of those directories will ultimately correspond to the categories in the inventory.

For example, if the composer wanted to allocate all the *Hi-Hat* samples in the current directory under a category of *Percussion*, they could issue the command:

.. code-block:: bash
		
   genercat -D Percussion -C Hi-Hat

This would have the effect of creating a *Percussion* subdirectory (unless it already existed) and moving all the files with the *Hi-Hat* string in their file name into that subdirectory. This could be repeated as much as the composer saw fit:

.. code-block:: bash

   genercat -D Percussion -C Snare
   genercat -D Percussion -C Topper
   genercat -D Percussion -C Riser

Where the mapping is even simpler, and the category name matches the string name, a shorter version of the command can be issued:

.. code-block:: bash

   genercat -C Synth

which moves all the files with *Synth* in their filename down into a *Synth* category, assuming the destination is a direct mapping from the **-C** specification supplied.

As the diagram illustrates, some or all of this organisation can be achieved using manual or other scripting operations. The genercat_ utility is provided as a convenience utility only.

The key objective is to ensure that the categorised sample files are ultimately held in a directory named after the category itself:

.. code-block:: bash

   /full/path/to/this/set/is/Drums/My Drum Sample 01.wav
   /full/path/to/this/set/is/Drums/My Drum Sample 02.wav
   /full/path/to/a/different/set/is/Drums/Daves Drum Sample 01.wav
   /full/path/to/some/other/set/is/Drums/Bobs Drum Sample 01.wav
   /full/path/to/free/samples/dRUMS/My Drum Sample 01.wav
   /full/path/to/this/set/is/drums/My Drum Sample 03.wav

The key things to note are:

    #. It is the penultimate element of the full pathname to the sample file is used to determine the category in later operations
    #. The category string as it appears in the path is case-insensitive - e.g. *DRUMS*, *dRUms* or *drums* will each map to the *Drums* category when inventoried
    #. The filename of the sample file does not need to be unique because the reference will always be a full path.

To illustrate this workflow with a worked example, I am going to create a very small sample library under `/tmp/samples`:

.. code-block:: bash

   cd /tmp/samples
   ls | sort
   
   City_Lights_Gated_Bass.wav
   City_Nights_Bass.wav
   City_of_Angeles_Sub_Bass.wav
   Daylight_Beat_01.wav
   Daylight_Beat_02.wav
   Endless_Streets_Acoustic_Bass_Chops.wav
   Endless_Streets_Bass_Swell.wav
   Endless_Streets_Stabby_Bass.wav
   Endless_Streets_Sub_Bass_01.wav
   Endless_Streets_Sub_Bass_02.wav
   Head_to_Head_Beat_01.wav
   Head_to_Head_Beat_02.wav
   Recollection_Atmo_Pads.wav
   Recollection_Bell_Pads.wav
   Recollection_Pad_01.wav
   Recollection_Pad_02.wav
   Recollection_Pulsing_Pads.wav
   Recollection_Vox_Pads.wav

This is then categorised, thus:

.. code-block:: bash
   
   genercat -C Bass
   genercat -C Pad
   genercat -C Beat

   tree .
   .
   ├── Bass
   │   ├── City_Lights_Gated_Bass.wav
   │   ├── City_Nights_Bass.wav
   │   ├── City_of_Angeles_Sub_Bass.wav
   │   ├── Endless_Streets_Acoustic_Bass_Chops.wav
   │   ├── Endless_Streets_Bass_Swell.wav
   │   ├── Endless_Streets_Stabby_Bass.wav
   │   ├── Endless_Streets_Sub_Bass_01.wav
   │   └── Endless_Streets_Sub_Bass_02.wav
   ├── Beat
   │   ├── Daylight_Beat_01.wav
   │   ├── Daylight_Beat_02.wav
   │   ├── Head_to_Head_Beat_01.wav
   │   └── Head_to_Head_Beat_02.wav
   └── Pad
       ├── Recollection_Atmo_Pads.wav
       ├── Recollection_Bell_Pads.wav
       ├── Recollection_Pad_01.wav
       ├── Recollection_Pad_02.wav
       ├── Recollection_Pulsing_Pads.wav
       └── Recollection_Vox_Pads.wav

   


Creating the sample inventory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you are satisfied that your sample libraries are organised in the way you want, it is time to create the inventory file from which you will be selecting samploes with your algorithms. To do this you use the generinv_ utility in the directory in which you intend to run the **generiter** command eventually. For this simple demonstration, assuming your sample tree is rooted in `/tmp/samples` the basic command would look something like:

.. code-block:: bash
		
   cd $HOME
   generinv -I /tmp/samples -o inventory

This creates an `inventory.json` file that will look like:

.. code-block:: json

   {
        "Bass":{
            "/tmp/samples/Bass/City_Lights_Gated_Bass.wav":true,
	    "/tmp/samples/Bass/City_Nights_Bass.wav":true,
	    "/tmp/samples/Bass/City_of_Angeles_Sub_Bass.wav":true,
	    "/tmp/samples/Bass/Endless_Streets_Acoustic_Bass_Chops.wav":true,
	    "/tmp/samples/Bass/Endless_Streets_Bass_Swell.wav":true,
	    "/tmp/samples/Bass/Endless_Streets_Stabby_Bass.wav":true,
	    "/tmp/samples/Bass/Endless_Streets_Sub_Bass_01.wav":true,
	    "/tmp/samples/Bass/Endless_Streets_Sub_Bass_02.wav":true
	    },
	"Beat":{
            "/tmp/samples/Beat/Daylight_Beat_01.wav":true,
	    "/tmp/samples/Beat/Daylight_Beat_02.wav":true,
	    "/tmp/samples/Beat/Head_to_Head_Beat_01.wav":true,
	    "/tmp/samples/Beat/Head_to_Head_Beat_02.wav":true
	},
	"Pad":{
	    "/tmp/samples/Pad/Recollection_Atmo_Pads.wav":true,
	    "/tmp/samples/Pad/Recollection_Bell_Pads.wav":true,
	    "/tmp/samples/Pad/Recollection_Pad_01.wav":true,
	    "/tmp/samples/Pad/Recollection_Pad_02.wav":true,
	    "/tmp/samples/Pad/Recollection_Pulsing_Pads.wav":true,
	    "/tmp/samples/Pad/Recollection_Vox_Pads.wav":true
	}
    }
   
Creating the composer control file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generating music
^^^^^^^^^^^^^^^^

.. _genercat: genercat_cli.html
.. _generinv: generinv_cli.html
.. _generiter: generiter_cli.html

