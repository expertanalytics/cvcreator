CV Creator is an automated curriculum vitae (CV) generator which uses TOML
templates.

Its primary usage is to standardize Expert Analytics' (XAL) employee CVs, but it
can be used for creating CV without the company branding for private use as
well.

.. contents:: Table of Contents

Installation
============

The main CV Creator tool is created in `Python <https://python.org>`_ and can be
install through ``pip``.
See `this guide <https://packaging.python.org/tutorials/installing-packages>`_
for help to get ``pip`` working on your system.

With this repository cloned to disk, and `Python <https://python.org>`_ and ``pip`` in place, install CV Creator through:

.. code:: sh

  pip install cvcreator

The tool depend on a working installation of Latex:

* Windows -- `Install Miktex <https://miktex.org/download>`_.
* Debian/Ubuntu -- run ``sudo apt-get install texlive-latex-extra texlive-lang-european``.
* Arch -- run ``sudo pacman -Syu texlive-latexextra texlive-lang``.
* Mac OSX -- `Install Homebrew <https://brew.sh>`_ and run ``brew install --cask mactex``.

Basic usage
===========

Start by creating a simple example:

.. code:: sh

  cv example example.toml

Edit the resulting ``example.toml`` file with your favorite text editor.
This is the content file which will be inserted into the final CV output.
The different sections should be self-explanatory.

With the content ready, create a CV with:

.. code:: sh

  cv create example.toml my_new_cv.pdf

It will look something like this:

.. image:: https://raw.githubusercontent.com/expertanalytics/cvcreator/master/example.jpg 
  :align: center
  :width: 300px

Projects and publications
=========================

To include projects/publications use the flag ``--publications``/``--projects``.
These flags must be followed by specific tags present in the toml content file:

.. code:: sh

  cv create example.yaml --projects "A1,A2"
  cv create example.yaml --publications "P1,P2"

The projects/publications will be added in selected order.
Alternatively, use a colon ``:`` to include all entries.

.. code:: sh

  cv create example.yaml --publications :

.. note::

  You will need to add flags to include projects and publications.
  If omitted none will be include.

Custom logo
===========

There are currently two components that are Expert Analytic:

* The logo image in the upper right corner of the first document.
* The footer image on each page.

These two elements can be overridden through the ``.toml`` content file.
Add the following two lines to the top of the file (outside a title scope):

.. code:: toml

  logo_image = "path/to/image.png"
  footer_image = "path/to/image.png"

These can be any images, but it perhaps makes sense that the ``logo_image`` is
a personal photo when using the tool privately.

Technology skills
=================

To be able to do statistics on various skills, the list of allowed skills is
limited to a predefined list. To quickly list what skills are allowed, and
their spelling, see::

  cv skills

In addition, some skills have badges that can be activated during document
creation using the ``--badges`` flag with e.g. ``cv create`` and ``cv latex``.
To list which skill can produce an icon, see::

  cv skills --badges


Adding new skills and badges
----------------------------

If a skill is missing, or a skill is written in an incorrect way, please either
`file an issue <https://github.com/expertanalytics/cvcreator/issues>`_ or
`make a request <https://github.com/expertanalytics/cvcreator/pulls>`_ with 
the proposed change. In the latter case, the changes can be made to the file:
``cvcreator/templates/tech_skills.toml``.

In addition, if there is a badge that is missing (or needs replacing) here is
useful checklist:

* Find a badge candidate, consisting of simple pure black vector graphics
  formatted as a ``.pdf`` file. Be wary that some tools will convert vector
  graphics to raster when coverting.
* There should not be any copyright issues with the badge. Most badges are
  currently `CC0
  <https://creativecommons.org/share-your-work/public-domain/cc0/>`_.
* Place the badge in the folder ``cvcreator/icons``.
* Except for the ``.pdf`` extension, the name must exactly match that of the
  badge trigger. This means include capitalized letters and spaces.

Developer Guide
===============

The project uses `poetry`_ to manage its development installation. Assuming
`poetry`_ installed on your system, installing ``cvcreator`` for development
can be done from the repository root with the command:

.. code-block:: bash

    poetry install

This will install all required dependencies and cvcreator into a virtual
environment. To enter the create environment, run:

.. code-block:: bash

    poetry shell

Afterwards exit with:

.. code-block:: bash

    exit

.. _poetry: https://poetry.eustace.io/

Testing
-------

To ensure that the code run on your local system, run the following:

.. code-block:: bash

    poetry run pytest --doctest-modules cvcreator/ test/

Deployment
==========

Releases to PyPI (the repository used when using ``pip install``) is created
and deployed automatically when making a tagged released. To do so you need to:

* Update and push a new version number in ``pyproject.toml`` to branch ``master``.

After merging to master, the workflow creates the tag and Github release for 
this version and uploads its wheel file to Pypi.
