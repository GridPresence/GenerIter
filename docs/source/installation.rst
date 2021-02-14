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

Installation
============

Installing on macOS
-------------------

GenerIter requires Python 3.6+ but older versions of macOS only had Python 2.7. First determine if you're running 3.x or 2.x: Open up the command line via the Terminal application which is located at Applications -> Utilities -> Terminal.

In the terminal, at the `$` prompt, enter the following command, and look at the output:

.. code-block:: bash

   $ python --version
   Python 2.7.17


If this is version 2.x, continue, if it's 3.x, skip down to 'Installing via pip'

Installing Python 3.x
^^^^^^^^^^^^^^^^^^^^^

To update macOS's version of Python, we'll use the tool [Homebrew](brew.sh), to do this, cut and paste the following command into your terminal, and press 'Enter'

.. code-block:: bash

   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


This will install Apple's Xcode commandline tools and other required software, it could take up to 5 minutes to complete. When this is done, initialize and test that `homebrew` is installed and working:

.. code-block:: bash

   brew doctor


If that's successful, use `homebrew` to install Python 3.9:

.. code-block:: bash

   brew install --build-from-source python@3.9


This command will take longer than the last one, as it's going to build Python from source.

Installing via pip
^^^^^^^^^^^^^^^^^^

Now we'll use `pip`, a package manger for Python, to install generiter

.. code-block:: bash

   pip3 install generiter


Installing on Debian-derived Linux
----------------------------------

Generiter requires Python 3.6+ which most recent version of Linux will have. First determine if you're running 3.x or 2.x: Open up terminal application in Linux, and prompt, enter the following command, and look at the output:

.. code-block:: bash

   $ python --version
   Python 2.7.17


If you see a version of Python starting with a 2, such as Python 2.7.10, then try the same command using python3 instead of python, it's possible both will be installed.

If it's not and you only have version 2.x, continue, if it's 3.x, skip down to 'Installing generiter via pip'

### GNU Debian Linux and Ubuntu Linux

Install Python 3.x as defined at [Install Python](https://installpython3.com/linux/), by using the deadsnakes PPA:

.. code-block:: bash
   
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt-get update
   sudo apt install python3.8

Now we'll use `pip`, a package manger for Python, to install generiter

.. code-block:: bash

   pip3 install generiter


Installing on Arch Linux
------------------------

Install Python 3.x via `pacman`:

.. code-block:: bash

   pacman -S python3


Now we'll use `pip`, a package manger for Python, to install generiter

.. code-block:: bash

   pip3 install generiter


Installing on Windows
---------------------

Install Python 3.x as defined at [Install Python](https://installpython3.com/windows/)

Open Powershell, and run the following command:

.. code-block:: bash

   pip3 install generiter


Advanced Installation Notes
---------------------------

The **GenerIter** package uses `pydub <https://github.com/jiaaro/pydub/blob/master/API.markdown>`_, a dependency which should be satisfied during the package installation.

However, **pydub** has a partial dependency on `FFmpeg <https://ffmpeg.org/>`_

At the moment we only use **WAV** format audio throughout, so the package will work without this dependency and only generate a benign warning. Ultimately we wish to be able to transparently convert into and out of other formats (e.g. **mp3**, **FLAC**, etc.). In order to use that functionality, you will need to install `FFmpeg <https://ffmpeg.org/>`_ on your machine later.

The source for the GenerIter package can also be found on `GitHub <https://github.com/GridPresence/GenerIter>`_.
