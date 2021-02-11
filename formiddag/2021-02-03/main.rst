:css: main.css

.. title:: Anbefalinger rundt hvordan sette opp og bruke et Python-prosjekt


Python environments can be a mess.
==================================

.. image:: ./xkcd_python.png

----

Presentation overview
---------------------

* Handling multiple versions of Python.
* ``pip`` installable that are meant as a shell tool.
* The old way of the virtual environments.
* The new way forward.

----

Don't use system Python if you can.
===================================

System Python, e.g. ``/usr/bin/python``, is not for development.

* It is often quite old on many systems.
* It is often hard/not possible to upgrade later.
* If you screw up, you might screw your system up in the process.

So only use it to install tools you need on your system.

----

``pyenv``: Install and managing multiple Python versions local to the user.
===========================================================================

* Compiles to your system as if you would manually.
* Includes CLI for management.
* Store everything in a git-folder.

Source: https://github.com/pyenv/pyenv

----

``pipx``: Python command line tools that you need "everywhere".
===============================================================

* Same syntax as ``pip``.
* Creates isolated virtual environments for each install.
* Soft links to CLI in the folder ``~/.local/bin/``.

Source: https://github.com/pipxproject/pipx

----

``venv``: Isolating Python through virtual environments.
========================================================

* Makes a copy of Python binaries and libraries into a folder.
* Includes activation/deactivation scripts for changing path handle to Python.
* Designed to allow for a copy for each project.

----

Virtual environments are not without flaws.
===========================================

* Python binaries are typically redundant to copy over.
* Activation/deactivation is cumbersome and easy to forget.
* Patch updates of Python requires full reinstall.
* Poor support for nested environments.
* ``$PATH`` manipulation is frown upon. (It should be ``$PYTHONPATH``.)

----

Steering console is trying to fix Python management.
====================================================

Python is changed through Python environment proposals (PEP), and there have
been a lot of those lately:

* https://www.python.org/dev/peps/pep-0508/
* https://www.python.org/dev/peps/pep-0517/
* https://www.python.org/dev/peps/pep-0518/
* https://www.python.org/dev/peps/pep-0582/
* https://www.python.org/dev/peps/pep-0621/
* https://www.python.org/dev/peps/pep-0631/

----

Except ``cpython`` PEPs are only specification.
===============================================

Community responsible to follow the specification:

.. code:: sh

  pip
  setuptools
  pipenv
  poetry
  pyflow
  pdm

----

``pdm``: Ahead of the curve in following the PEPs.
==================================================

* One stop tool for managing a Python project.

Source: https://pdm.fming.dev/

----

``pyproject.toml``: A declarative way to define dependencies.
=============================================================

----

``dependencies``, ``dev-dependencies`` and ``requires``: Categorizing project dependencies.
===========================================================================================

----

``__pypackages__``: Folder based dependency handling.
=====================================================

----

``pdm.lock``: Fully reproducible installation.
==============================================

----

``[project.scripts]``: Making your own console scripts.
=======================================================

----

``build.py``: Make C extensions.
================================
