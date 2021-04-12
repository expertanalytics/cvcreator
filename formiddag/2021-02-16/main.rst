:css: main.css

Why Pandas is primarily for experimenting, and Numpy for production.
====================================================================

By Jonathan Feinberg, 16-02-2021

----

Need-for-speed: Where ``numpy`` and ``pandas`` overlap.
=======================================================

----

Data scientist usually bound more by memory and IO, than computational cost.
============================================================================

----

Let us assume to have some data to manage.
==========================================

.. code:: python

  numbers = list(range(10**6))
  strings1 = [f"{idx}" for idx in numbers]
  strings2 = [f"${idx}" for idx in numbers]

----

Declaring data into correct format.
===================================

.. code:: python

  import pandas
  import numpy

  frame = pandas.DataFrame({
    "numbers" = numbers,
    "strings1" = strings1,
    "strings2" = strings2,
  })

  dtype = numpy.dtype([("numbers", "i"), ("strings1", "U6"), ("strings2", "U7")])
  array = numpy.empty(10**6, dtype=dtype)
  array["numbers"] = numbers
  array["strings1"] = strings1
  array["strings2"] = strings2

----

Data usage is up to *3 times higher* for ``pandas``.
====================================================

.. code:: python

  frame.memory_usage(True, True).sum()/1024**2

  array.nbytes/1024**2

----

Shenanigans involving numbers and strings.
==========================================

.. code:: python

  frame.loc[:4, "numbers"] = frame.loc[:4, "strings1"]

  frame.loc[:4, "numbers"] = frame.loc[:4, "strings2"]

  array["numbers"][:4] = array["strings1"][:4]

  array["numbers"][:4] = array["strings2"][:4]

----

Underneath the hood strings are very different.
===============================================

----

``pandas.DataFrame.join`` is super convenient.
==============================================

Pandas:

onco/amb/amb/binding/data

Numpy:

onco/oiml/oiml/convert/chain_sequence.py

----

Chunking data with ``h5py``.
============================
