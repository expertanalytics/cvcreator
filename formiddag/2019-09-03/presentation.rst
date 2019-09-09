:title: How to squeeze a polynomial into a numpy datatype
:data-transition-duration: 500

How to squeeze a polynomial into a numpy datatype
=================================================

By Jonathan Feinberg


----

:data-x: r1000
:data-y: r0

Background: Chaospy use polynomial model approximation
======================================================

.. code:: python

   >>> distribution = chaospy.J(chaospy.Uniform(1, 2), chaospy.Uniform(0.1, 0.2))
   >>> polynomial_expansion = chaospy.orth_ttr(2, distribution)
   >>> print(polynomial_expansion)
   [1.0, q1-0.15, q0-1.5, q1^2-0.3q1+0.0216667,
    q0q1-0.15q0-1.5q1+0.225, q0^2-3.0q0+2.16667]

----

Primitive solutions: Dicts and Numpy
====================================

Place numerical arrays into polynomial coefficients:

.. code::

   +--+--+--+     +--+--+--+        +--+--+--+
   | 1| 2| 3|     | 5| 6| 7|        | 7| 6| 5|
   +--+--+--+  +  +--+--+--+ q0  +  +--+--+--+ q0 q1^2  +  ...
   | 2| 4| 6|     | 2| 4| 6|        | 2| 4| 6|
   +--+--+--+     +--+--+--+        +--+--+--+

In practice:

.. code:: python

   >>> print(polynomial_expansion)
   [1.0, q1-0.15, q0-1.5, q1^2-0.3q1+0.02167,
    q0q1-0.15q0-1.5q1+0.225, q0^2-3.0q0+2.16667]
   >>> print(polynomial_expansion.A)
   {(0, 1): array([0.,  1.,    0.,  -0.3,    -1.5,   0.]),
    (0, 0): array([1., -0.15, -1.5,  0.02167, 0.225, 2.16667]),
    (0, 2): array([0.,  0.,    0.,   1.,      0.,    0.]),
    (2, 0): array([0.,  0.,    0.,   0.,      0.,    1.]),
    (1, 0): array([0.,  0.,    1.,   0.,     -0.15, -3.]),
    (1, 1): array([0.,  0.,    0.,   0.,      1.,    0.])}

----

Approach has a lot of problems
==============================

* Maintenance burden:

  .. code:: python

    >>> polynomial_expansion.reshape(2, 3)

* No numpy compatibility:

  .. code:: python

    >>> numpy.sum(polynomial_expansion)  # fails

* Order of operations not always intuitive:

  .. code:: python

    >>> [0, 1, 2, 3, 4, 5] - polynomial_expansion              # Poly
    >>> numpy.array([0, 1, 2, 3, 4, 5]) - polynomial_expansion # numpy object type

----

Where is there room to place a full polynomial?
===============================================

.. image:: ./dtype-hierarchy.png

----

Flexible dtype ``void`` is used for Structured Arrays
=====================================================

.. code:: python

   >>> dtype = numpy.dtype([("name", "U20"),
   ...                      ("awesome", "b"),
   ...                      ("style", "i8")])

   >>> data = numpy.zeros(3, dtype=dtype)
   >>> data["name"] = "Ola", "Alocias", "Jonathan"
   >>> data["awesome"] = 1, 1, 0
   >>> data["style"] = 4, 9000, 2

   >>> print(data)
   [('Ola', 1,    4) ('Alocias', 1, 9000) ('Jonathan', 0,    2)]

----

Warning -- Serious Hack attempt ahead
=====================================

----

Masking structured array as polynomial
======================================

Use printable string values as substitute for numbers:

.. code:: python

   >>> from string import printable
   >>> print(printeable)
   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJK...

   >>> FORWARD_DICT = dict(enumerate(numpy.array(list(printable), dtype="U1")))
   >>> FORWARD_MAP = numpy.vectorize(FORWARD_DICT.get)

   >>> exponents = numpy.array([[0, 0], [0, 1], [1, 0]])
   >>> exponents_as_strings = FORWARD_MAP(exponents).flatten().view("U2")
   >>> print(exponents_as_strings)
   ['00' '01' '10']

   >>> INVERSE_DICT = {value: key for key, value in FORWARD_DICT.items()}
   >>> INVERSE_MAP = numpy.vectorize(INVERSE_DICT.get)

   >>> print(INVERSE_MAP(exponents_as_strings.view("U1").reshape(-1, 2)))
   [[0 0]
    [0 1]
    [1 0]]

----

Sublcassing ``numpy.ndarray`` is easy
=====================================

.. code:: python

   class ndpoly(numpy.ndarray):

      __array_priority__ = 16

      _dtype = None
      _exponents = None
      _indeterminants = None

      def __new__(
               cls,
               exponents=((0,),),
               shape=(),
               indeterminants="z",
               dtype=None,
               **kwargs
      ):
         exponents = numpy.array(exponents, dtype=int)
         dtype_ = "S%d" % exponents.shape[1]

         # ...

         exponents = FORWARD_MAP(exponents).flatten()
         exponents = numpy.array(exponents.view(dtype_), dtype="U")

         dtype = int if dtype is None else dtype
         dtype_ = numpy.dtype([(key, dtype) for key in exponents])

         obj = super(ndpoly, cls).__new__(cls, shape=shape, dtype=dtype_, **kwargs)

         obj._dtype = dtype
         obj._exponents = exponents
         obj._indeterminants = tuple(indeterminants)
         return obj

----

:data-x: r0
:data-y: r500

.. code:: python

      def __array_finalize__(self, obj):
         if obj is None:
               return
         self._exponents = getattr(obj, "_exponents", None)
         self._indeterminants = getattr(obj, "_indeterminants", None)
         self._dtype = getattr(obj, "_dtype", None)

----

:data-x: r1000
:data-y: r-500

We can store, but how about manipulations?
==========================================

.. code:: python

   # ...
      def __array_ufunc__(self, ufunc, method, *args, **kwargs):

         # ...
         if ufunc not in array_function.ARRAY_FUNCTIONS:
            return super(ndpoly, self).__array_ufunc__(
               ufunc, method, *args, **kwargs)
         return array_function.ARRAY_FUNCTIONS[ufunc](*args, **kwargs)


   @implements(numpy.add)
   def add(x1, x2):
      x1, x2 = numpoly.align_polynomials(x1, x2)
      collection = x1.todict()
      for exponent, coefficient in x2.todict().items():
         collection[exponent] = collection.get(exponent, False)+coefficient
      exponents = sorted(collection)
      coefficients = [collection[exponent] for exponent in exponents]
      return numpoly.polynomial_from_attributes(
         exponents, coefficients, x1._indeterminants)

----

:data-x: r1000
:data-y: r0

Cherry on top: Numpy function compatibility!
============================================


.. code:: python

    def __array_function__(self, func, types, args, kwargs):
        if func not in array_function.ARRAY_FUNCTIONS:
            return super(ndpoly, self).__array_function__(
                func, types, args, kwargs)
        return array_function.ARRAY_FUNCTIONS[func](*args, **kwargs)

----

But does it work?
=================
