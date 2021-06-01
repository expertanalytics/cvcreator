CV Creator is an automated curriculum vitae (CV) generator which uses TOML
templates.

Its primary usage is to standardize Expert Analytics' (XA) employee CVs, but it
can be used for creating CV without the company branding for private use as
well.

.. contents:: Table of Contents

Installation
============

The main CV Creator tool is created in `Python <https://python.org>`_ and can be
install through ``pip``.
See `this guide <https://packaging.python.org/tutorials/installing-packages>`_
for help to get ``pip`` working on your system.

With `Python <https://python.org>`_ and ``pip`` in place, install CV Creator
through:

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

  cv toml example.toml

Edit the resulting ``example.toml`` file with your favorite text editor.
This is the content file which will be inserted into the final CV output.
The different sections should be self-explanatory.

With the content ready, create a CV with:

.. code:: sh

  cv create example.toml my_new_cv.pdf

It will look something like this:

.. raw:: html

  <img src="./example.jpg" width="300">

Projects and publications
=========================

To include projects/publications use the flag ``--publications``/``--projects``.
Can either be called with specific tags:

.. code:: sh

  cv create example.yaml --projects "A1,foo,whatever"

The tags are defined in the ``.toml`` content file.

The projects/publications will be added in selected order.
Use a colon ``:`` to include all entries.

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

Technology skill badges
=======================

When listing up technology skills, there will in some cases be an icon on the
left of the skill. These icons (or badges) pop up when a trigger word is used.
To list the current list of badges:

.. code:: sh

  cv badges

If there is a badge that is missing and you want to add it, please submit an
`issue <https://github.com/expertanalytics/cvcreator/issues>`_ with a request,
or more preferable submitting a
`pull request <https://github.com/expertanalytics/cvcreator/pulls>`_ with a
badge. If you do the latter:

* Find a badge candidate, consisting of simple pure black vector graphics
  formatted as a ``.pdf`` file. Be wary that some tools will convert vector
  graphics to raster when coverting.
* There should not be any copyright issues with the badge. Most badges are
  currently `CC0
  <https://creativecommons.org/share-your-work/public-domain/cc0/>`_.
* Place the badge in the folder `cvcreator/icons`.
* Except for the ``.pdf`` extension, the name must exactly match that of the
  badge trigger. This means include capitalized letters and spaces.
