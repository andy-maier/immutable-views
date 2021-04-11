"""
immutable-views - Immutable views on other collection objects
"""

from __future__ import absolute_import

from ._dict_view import *  # noqa: F403,F401
from ._list_view import *  # noqa: F403,F401
from ._set_view import *  # noqa: F403,F401
from . import _version

#: The full version of this package including any development levels, as a
#: :term:`string`.
#:
#: Possible formats for this version string are:
#:
#: * "M.N.P.dev1": Development level 1 of a not yet released version M.N.P
#: * "M.N.P": A released version M.N.P
__version__ = _version.__version__
