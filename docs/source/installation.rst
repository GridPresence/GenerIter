Introduction
============

.. toctree::
   :maxdepth: 2

Overview
--------

The **GenerIter** package is a software development kit (SDK) with which Python coders can manipulate sampled sounds programmatically to create new generative and iterative compositions.

The SDK is designed in such a way that it does all the heavy lifting of organising sample library contents according to whatever criteria makes sense to the composer, and then applying generative algorithms to those libraries using randomised or directed selection techniques.

The objective of the SDK is to give the composer some powerful assistance without constraining or dictating the creative aspects of their projects. To that end, you will find the SDK fairly lightweight in its implementation, but very configurable and agnostic about workflows and processes.

One of the key features of the package is that, although supplied with a set of example processors and algorithms for the novice user to start getting quick results, there is a simple facility that allows the composer-programmer to extend, replace, organise and control whatever algorithmic processes they wish to apply to their sample library external to the example processors we provide.

The only pre-requisite for achieving this flexibility is that the user has sufficient knowledge of Python 3.6, or later, with which to implement their algorithms.

Installing GenerIter
--------------------

The **GenerIter** package uses `pydub <https://github.com/jiaaro/pydub/blob/master/API.markdown>`_, a dependency which should be satisfied during the package installation.

However, **pydub** has a partial dependency on `FFmpeg <https://ffmpeg.org/>`_

If you only wish to use **WAV** format audio throughout, the package will work without this dependency. However, if you wish to be able to transparently convert into and out of other formats (e.g. **mp3**, **FLAC**, etc.) you will need to install `FFmpeg <https://ffmpeg.org/>`_ on your machine.

Installing **GenerIter** is as simple as typing:

.. code-block:: bash
		
   pip install GenerIter

If you have a previous version installed, you type:

.. code-block:: bash

   pip install --upgrade GenerIter

The source for the package can also be found on `GitHub <https://github.com/GridPresence/GenerIter>`_.
