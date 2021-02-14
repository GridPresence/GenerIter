Tutorials
=========

**Important Note** :

This module currently depends on the **pydub** module for manipulating audio segments in memory. The nature of the **pydub** implementation is such that it can hog memory, particularly if your algorithm doesn't clear redundant references to "old" immutable audio segments. This means that there may be occasions where you can be throwing "out of memory" exceptions.

This is not a **GenerIter** defect, but a **pydub** design flaw.

As a **GenerIter** user, it should be possible to ameliorate this problem by using smaller samples, sample sets and reducing the configuration workload. Future enhancements to **GenerIter** include a plan to replace **pydub** with something that manages memory better and minimises the likelihood of hitting this problem.

.. toctree::
   :maxdepth: 2

   basic_workflow
   advanced_grooving
   roll_your_own_algorithms
