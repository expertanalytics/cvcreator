"""
cvparser library
----------------

A library for automated create CV on the fly.
"""

from .parser import *     # noqa: ignore starred import here
from .workspace import *  # noqa: ignore starred import here

__all__ = parser.__all__ + workspace.__all__
