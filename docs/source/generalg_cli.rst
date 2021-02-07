
generalg
--------

.. code:: bash

   usage: generalg [-h] -A A -M M -L L
       
   optional arguments:
      -h, --help  show this help message and exit
      -A A        Algorithm name
      -M M        Module name
      -L L        Library name

This is a helper utility that generates code stubs when you want to create a local module with hooks onto which new algorithms can be developed.

Thus:

.. code:: bash
   
   generalg -L testlib -M testmod -A testalg

will ensure that a directory named **testlib** is created.

Within **testlib**, the app ensures that the **__init__.py** and **Testmod.py** files exist.

**Note :** Only the library name is case-sensitive. All other parameters will be pushed into lower case and the module name will be capitalized.

The **Testmod.py** will contain:

.. code:: python

   from GenerIter.process import Process
   
   class Testmod(Process):
   
       def __init__(self):
	  super().__init__()
       
       
       def testalg(self):
	  print("Executing testalg")
	  # Your code goes here

