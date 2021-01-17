Basic Workflow
--------------

This text uses MacOS/Linux-style pathnames throughout. The code has been written such that it should also support DOS-style paths in a Windows-based command shell.

To illustrate this workflow with a worked example, I am going to create a very small sample library under `/tmp/samples` using the WAV samples provided `Archive.org`_.
Note that the "GenerIter_Demo_Track" files should be moved into a different directory outside the `/tmp/samples` tree as they are not used here.

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

This first phase assumes the you starts with an unstructured set of samples in youre directory.

To make the most out of the inventory classification system, it helps if the samples are organised in subdirectories named after the categories the composer finds useful. These category names can be clompletely arbitrary, but for this illustration I am going to use musical voice/instrument category specifiers like "Drums", "Bass", "Synths", etc.

The good news is that these categories can be specified at any level in your sample tree and don't require the "Drums" samples, for example to all be in a single directory.

The genercat_ utility is a helper command that allows the composer to allocate sets of sample files into named subdirectories, where the names of those directories will ultimately correspond to the categories in the inventory.


To illustrate this workflow with a worked example, I am going to create a very small sample library under `/tmp/samples` using the WAV samples I downloaded from `Archive.org`_:

.. code-block:: bash

   cd /tmp/samples
   .
   ├── Bass_1.wav
   ├── Bass_2.wav
   ├── Bass_3.wav
   ├── Beats_1.wav
   ├── Beats_2.wav
   ├── Beats_3.wav
   ├── Drone_1.wav
   ├── Drone_2.wav
   ├── Drone_3.wav
   ├── Guitar_1.wav
   ├── Guitar_2.wav
   ├── Guitar_3.wav
   ├── Organ_1.wav
   ├── Organ_2.wav
   ├── Organ_3.wav
   ├── Pepper_1.wav
   ├── Pepper_2.wav
   ├── Pepper_3.wav
   ├── Saxophone_1.wav
   ├── Saxophone_2.wav
   └── Saxophone_3.wav

This is then categorised, thus:

.. code-block:: bash
   
   genercat -C Bass
   genercat -C Beats
   genercat -C Drone
   genercat -C Guitar
   genercat -C Pepper
   genercat -C Organ
   genercat -C Saxophone

resulting in a tree structure that looks like:

.. code-block:: bash
   
   .
   ├── Bass
   │   ├── Bass_1.wav
   │   ├── Bass_2.wav
   │   └── Bass_3.wav
   ├── Beats
   │   ├── Beats_1.wav
   │   ├── Beats_2.wav
   │   └── Beats_3.wav
   ├── Drone
   │   ├── Drone_1.wav
   │   ├── Drone_2.wav
   │   └── Drone_3.wav
   ├── Guitar
   │   ├── Guitar_1.wav
   │   ├── Guitar_2.wav
   │   └── Guitar_3.wav
   ├── Organ
   │   ├── Organ_1.wav
   │   ├── Organ_2.wav
   │   └── Organ_3.wav
   ├── Pepper
   │   ├── Pepper_1.wav
   │   ├── Pepper_2.wav
   │   └── Pepper_3.wav
   └── Saxophone
       ├── Saxophone_1.wav
       ├── Saxophone_2.wav
       └── Saxophone_3.wav
   


Creating the sample inventory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you are satisfied that your sample libraries are organised in the way you want, it is time to create the inventory file from which you will be selecting samploes with your algorithms.

To do this you use the generinv_ utility in the directory in which you intend to run the **generiter** command eventually.

**Top Tip -** It's a good idea to keep your inventory and composer files away from your sample library, just to avoid cluttering the library up with spurious files.

For this simple demonstration, assuming your sample tree is rooted in `/tmp/samples` the basic commands would look something like:

.. code-block:: bash
		
   cd $HOME
   generinv -I /tmp/samples -o inventory

This creates an `inventory.json` file that will look like:

.. code-block:: json

   {
        "Bass":{
            "/tmp/samples/Bass/Bass_1.wav":true,
	    "/tmp/samples/Bass/Bass_2.wav":true,
	    "/tmp/samples/Bass/Bass_3.wav":true
	},
	"Beats":{
	    "/tmp/samples/Beats/Beats_1.wav":true,
	    "/tmp/samples/Beats/Beats_2.wav":true,
	    "/tmp/samples/Beats/Beats_3.wav":true
	},
	"Drone":{
            "/tmp/samples/Drone/Drone_1.wav":true,
	    "/tmp/samples/Drone/Drone_2.wav":true,
	    "/tmp/samples/Drone/Drone_3.wav":true
	},
        "Guitar":{
            "/tmp/samples/Guitar/Guitar_1.wav":true,
	    "/tmp/samples/Guitar/Guitar_2.wav":true,
	    "/tmp/samples/Guitar/Guitar_3.wav":true
	},
	"Organ":{
            "/tmp/samples/Organ/Organ_1.wav":true,
	    "/tmp/samples/Organ/Organ_2.wav":true,
	    "/tmp/samples/Organ/Organ_3.wav":true
	},
	"Pepper":{
	    "/tmp/samples/Pepper/Pepper_1.wav":true,
	    "/tmp/samples/Pepper/Pepper_2.wav":true,
	    "/tmp/samples/Pepper/Pepper_3.wav":true
	},
	"Saxophone":{
            "/tmp/samples/Saxophone/Saxophone_1.wav":true,
	    "/tmp/samples/Saxophone/Saxophone_2.wav":true,
	    "/tmp/samples/Saxophone/Saxophone_3.wav":true
	}
   }

All the paths are absolute, which makes the inventory file fully movable to anywhere in your filesystem.
   
Creating the composer control file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first composer control file is going to be very simple. So, fire up the text editor of your choice and create a file called `compose.json` with the following content:

.. code-block:: json

   {
       "Basic" : {
           "beatsbassdrone" : {
               "tracks" : 20,
               "repeats" : 6
           }
       },
       "Globals" : {
	   "destination" : "<your path here>"
       }
   }

The **Globals** parameters are those that are literally global to the generiter instance when it runs. In this simplified form, you will need to supply it with the path of the directory into which your generated tracks will be created.

The top part of the composition file translates into

* "Basic" - use the *Basic* processor as defined in the generiter.processor library

* "beatsbassdrone" - use the *beatsbassdrone* method of the *Basic* processor (in pure Python terms this equates to calling *generiter.processor.Basic.beatsbassdrone()* through configuration)

* "tracks" - create 20 tracks in this run

* "repeats" - use up to 6 internal loop repeats for each track (controls the length of each output track for this method)

Generating music
^^^^^^^^^^^^^^^^

Finally, we get to generate some tracks, and for this we use `generiter`_ thus:

.. code-block:: bash
		
   generiter -L inventory.json -C compose.json

You can then watch as your tracks are generated into a time- and date-stamped subdirectory of your target directory. This allows you to do multiple runs without accidentally overwriting any earlier works.

Your compositions will come out looking like:

.. code-block:: bash

   20210117130701
   └── Basic
       ├── Basic_beatsbassdrone_00.wav
       ├── Basic_beatsbassdrone_01.wav
       ├── Basic_beatsbassdrone_02.wav
       ├── Basic_beatsbassdrone_03.wav
       ├── Basic_beatsbassdrone_04.wav
       ├── Basic_beatsbassdrone_05.wav
       ├── Basic_beatsbassdrone_06.wav
       ├── Basic_beatsbassdrone_07.wav
       ├── Basic_beatsbassdrone_08.wav
       ├── Basic_beatsbassdrone_09.wav
       ├── Basic_beatsbassdrone_10.wav
       ├── Basic_beatsbassdrone_11.wav
       ├── Basic_beatsbassdrone_12.wav
       ├── Basic_beatsbassdrone_13.wav
       ├── Basic_beatsbassdrone_14.wav
       ├── Basic_beatsbassdrone_15.wav
       ├── Basic_beatsbassdrone_16.wav
       ├── Basic_beatsbassdrone_17.wav
       ├── Basic_beatsbassdrone_18.wav
       └── Basic_beatsbassdrone_19.wav

As you will see, the naming of the files and the organisation of them follws the specification of the *compose.json* file, making them easy to navigate and understand. As your compositions become bigger and more complex, this will also allow you observe/extract interesting intermediate forms.

The Next Iteration
^^^^^^^^^^^^^^^^^^

That's all well and good, but it's only using 3 of the voices in your inventory. Let's explore a slightly more flexible algorithm **voices3**, which allows you to arbitrarily assign three difference voices from your inventory and then use those in exactly the same way.

Edit your *compose.json* to look like:

.. code-block:: json

   {
       "Basic" : {
       "beatsbassdrone" : {
           "tracks" : 20,
           "repeats" : 6
        },
	"voices3" : {
	    "tracks" : 20,
	    "repeats" : 6,
	    "voices" : [ "Beats",
        		 "Bass",
			 "Guitar" ]
	}
    },
        "Globals" : {
	    "destination" : "<your path here>"
	}
    }

As you can see, all that's happened is that a new *voices3* method of *Basic* is being invoked  and that method can be configured here to use an arbitrary set of 3 of the available voices, although in this example I have replaced the *Drone* voice with *Guitar*.

Running **exactly the same** *generiter* command

.. code-block:: bash
		
   generiter -L inventory.json -C compose.json

yields output arranged thus:

.. code-block:: bash
		
   20210117132943/
   └── Basic
       ├── Basic_beatsbassdrone_00.wav
       ├── Basic_beatsbassdrone_01.wav
       ├── Basic_beatsbassdrone_02.wav
       ├── Basic_beatsbassdrone_03.wav
       ├── Basic_beatsbassdrone_04.wav
       ├── Basic_beatsbassdrone_05.wav
       ├── Basic_beatsbassdrone_06.wav
       ├── Basic_beatsbassdrone_07.wav
       ├── Basic_beatsbassdrone_08.wav
       ├── Basic_beatsbassdrone_09.wav
       ├── Basic_beatsbassdrone_10.wav
       ├── Basic_beatsbassdrone_11.wav
       ├── Basic_beatsbassdrone_12.wav
       ├── Basic_beatsbassdrone_13.wav
       ├── Basic_beatsbassdrone_14.wav
       ├── Basic_beatsbassdrone_15.wav
       ├── Basic_beatsbassdrone_16.wav
       ├── Basic_beatsbassdrone_17.wav
       ├── Basic_beatsbassdrone_18.wav
       ├── Basic_beatsbassdrone_19.wav
       ├── Basic_voices3_00.wav
       ├── Basic_voices3_01.wav
       ├── Basic_voices3_02.wav
       ├── Basic_voices3_03.wav
       ├── Basic_voices3_04.wav
       ├── Basic_voices3_05.wav
       ├── Basic_voices3_06.wav
       ├── Basic_voices3_07.wav
       ├── Basic_voices3_08.wav
       ├── Basic_voices3_09.wav
       ├── Basic_voices3_10.wav
       ├── Basic_voices3_11.wav
       ├── Basic_voices3_12.wav
       ├── Basic_voices3_13.wav
       ├── Basic_voices3_14.wav
       ├── Basic_voices3_15.wav
       ├── Basic_voices3_16.wav
       ├── Basic_voices3_17.wav
       ├── Basic_voices3_18.wav
       └── Basic_voices3_19.wav

So, we have not only created a set of *voices3*-derived compositions, we have also created a new set of *beatsbassdrone*-derived compositions. These are not copies of the previous set, but a completely new set using the same algorithm, but with different random selections and decisions.

At this point, when you listen to all the outputs, you may start to hear a certain *same-y* quality to some of the outputs. It should be clear that, even with these very basic algorithms, the diversity and variation in your compositions is going to depend very much on the breadth and size of the sample sets in your libraries.

Another Iteration
^^^^^^^^^^^^^^^^^

Work In Progress - using more randomness to select N voices

Yet Another Iteration
^^^^^^^^^^^^^^^^^^^^^

Work Progress - using complete randomness to select a random number of voices

.. _genercat: genercat_cli.html
.. _generinv: generinv_cli.html
.. _generiter: generiter_cli.html
.. _Archive.org: https://archive.org/details/GenerIter

