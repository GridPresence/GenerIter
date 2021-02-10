Roll Your Own Algorithm
-----------------------

(For this tutorial, it is assumed that the user has a familiarity with Python programming terms and idioms.)

One of the design objectives of this module is to provide a framework into which users can extend and customise the algorithmic capabilities of the GenerIter command without touching the supplied code.

This is achieved through the use of the `GenerIter.Process` as an abstract base class from which new processors can be derived, encompassing the use of the Selector and Config classes and drivine the `generiter` app purely through data configuration.

For this tutorial a dummy `Process`-derived class will be implemented to illustrate the mechanism. For real generative audio algorithmic development, the user is encouraged to examine the existing algorithms and processors, and read the **pydub** API documentation, to understand and use the example implementations as references for further development. Feel free to cut and paste implementation fragments if they are useful.

Create your library module
^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example we want to create a new algorithm. Let's call it **local01**.

To do this, the algorithm needs to be attached to a **Process**-derived object, which we'll call **Myprocess**.

In order to access the object module at runtime, we need to put it in a library module. We'll call this **mylib**.

Pythonistas will be able to do this easily enough from the description above, but even then they are likely to make errors. To simplify the process and minimise basic system errors,the **GenerIter** module comes with its own code generator for local algorithm development, called **generalg**.

To achieve the structures described above:

.. code:: bash
   
   generalg -L mylib -M myprocess -A local01

will ensure that a directory named **testlib** is created.

Within **mylib**, the app ensures that the **__init__.py** and **Myprocess.py** files exist.

**Note :** Only the library name is case-sensitive. All other parameters will be pushed into lower case and the module name will be capitalized.

The **Myprocess.py** will contain:

.. code:: python

   from GenerIter.process import Process
   
   class Myprocess(Process):
   
       def __init__(self):
	  super().__init__()
       
       
       def local01(self):
	  print("Executing local01")
	  # Your code goes here

Testing your module
^^^^^^^^^^^^^^^^^^^

This is easy to test.

Create a simple **test.json** file:

.. code:: json

   {
       "Myprocess" : {
           "local01" : {
	   }
       }
   }

In the following example, the name of the inventory file is irrelevant - although it has to be there to satisfy the constraints of the application, no selection processing is specified so no output files will get generated.

To test the new library module:

.. code:: bash

   generiter -L someinventoryfile.json -C test.json -P mylib

This should produce the following output:

.. code:: bash

   mylib
   Process()
   Myprocess.local01()
   Executing local01

**Congratulations!!!** your new library and modules work.

It's not very interesting at the moment, but you have created a new algorithm. All you need to do now is fill in the missing code.


Further expansions
^^^^^^^^^^^^^^^^^^

The **generalg** utility is designed so that you can add new algorithms to existing processors:

.. code:: bash

   generalg -L mylib -M myprocess -A local02

Thus:

.. code:: python

   from GenerIter.process import Process

   class Myprocess(Process):

       def __init__(self):
           super().__init__()
	   
	   
       def local01(self):
	   print("Executing local01")
           # Your code goes here


       def local02(self):
           print("Executing local02")
           # Your code goes here


Add new processor modules to your library:

.. code:: bash

   generalg -L mylib -M anotherprocess -A algorithm

Or create a completely new library:

.. code:: bash

   generalg -L newlib -M anotherprocess -A algorithm


**However** it is NOT sufficiently smart to prevent you adding a repeat copy of the same algorithm name to the same processor module:

.. code:: bash

   generalg -L newlib -M anotherprocess -A algorithm
   generalg -L newlib -M anotherprocess -A algorithm

Will create:

.. code:: python

   from GenerIter.process import Process

   class Anotherprocess(Process):

       def __init__(self):
           super().__init__()
	   
	   
       def algorithm(self):
           print("Executing algorithm")
           # Your code goes here
	   
	   
       def algorithm(self):
           print("Executing algorithm")
           # Your code goes here

Which will throw a fatal Python exception when you try to use it.

