"""
An immutable dictionary view.
"""

from __future__ import print_function, absolute_import

import os
try:
    from collections.abc import Mapping, KeysView, ValuesView, ItemsView
except ImportError:
    # Python 2
    from collections import Mapping, KeysView, ValuesView, ItemsView
import six

__all__ = ['DictView']

# This env var is set when building the docs. It causes the methods
# that are supposed to exist only in a particular Python version, not to be
# removed, so they appear in the docs.
BUILDING_DOCS = os.environ.get('BUILDING_DOCS', False)


class DictView(Mapping):
    """
    An immutable dictionary view.

    Derived from :class:`~py3:collections.abc.Mapping`.

    This is an immutable view on an original (mutable) dictionary object.

    The view class supports the complete Python dictionary behavior, except for
    any operations that would modify the dictionary. More precisely, the view
    class supports all methods of :class:`~py3:collections.abc.Mapping`
    (the methods are listed in the table at the top of the linked page).

    The view is "live": Since the view class delegates all operations to the
    original dictionary, any modification of the original dictionary object
    will be visible in the view object.

    Note that only the view object is immutable, not its items. So if the keys
    or values in the original dictionary are mutable objects, they can be
    modified through the view.
    """

    def __init__(self, a_dict):
        """
        Parameters:

          a_dict (:class:`~py3:collections.abc.Mapping`):
            The original dictionary.
        """
        if not isinstance(a_dict, Mapping):
            raise TypeError(
                "The a_dict parameter must be a Mapping, but is: {}".
                format(type(a_dict)))
        self._dict = a_dict

    def __getitem__(self, key):
        """
        Return the value of the item in the original dictionary with an
        existing key.

        Raises:
          KeyError: Key does not exist.
        """
        return self._dict.__getitem__(key)

    def __len__(self):
        """
        Return the number of items in the original dictionary.
        """
        return self._dict.__len__()

    def __contains__(self, key):
        """
        Return a boolean indicating whether the original dictionary contains an
        item with the key.
        """
        return self._dict.__contains__(key)

    def __reversed__(self):
        """
        Return an iterator through the original dictionary in reversed iteration
        order.
        """
        return self._dict.__reversed__()

    def get(self, key, default=None):
        """
        Return the value of the item in the original dictionary with an existing
        key, or if the key does not exist, a default value.
        """
        return self._dict.get(key, default)

    def has_key(self, key):
        """
        Python 2 only: Return a boolean indicating whether the original
        dictionary contains an item with the key.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.has_key(key)  # noqa: W601

    # Iteration methods

    def keys(self):
        # pylint: disable=line-too-long
        """
        Return a view on (in Python 3) or a list of (in Python 2) the
        keys of the original dictionary in iteration order.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.keys()

    def values(self):
        # pylint: disable=line-too-long
        """
        Return a view on (in Python 3) or a list of (in Python 2) the
        values of the original dictionary in iteration order.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.values()

    def items(self):
        # pylint: disable=line-too-long
        """
        Return a view on (in Python 3) or a list of (in Python 2) the
        items of the original dictionary in iteration order, where each item
        is a tuple of its key and its value.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.items()

    def iterkeys(self):
        """
        Python 2 only: Return an iterator through the keys of the original
        dictionary in iteration order.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.iterkeys()

    def itervalues(self):
        """
        Python 2 only: Return an iterator through the values of the original
        dictionary in iteration order.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.itervalues()

    def iteritems(self):
        """
        Python 2 only: Return an iterator through the items of the original
        dictionary in iteration order, where each item is a tuple of its key
        and its value.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.iteritems()

    def viewkeys(self):
        # pylint: disable=line-too-long
        """
        Python 2 only: Return a view on the keys of the original dictionary
        in iteration order.

        See
        `Dictionary View Objects on Python 2 <https://docs.python.org/2/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.viewkeys()

    def viewvalues(self):
        # pylint: disable=line-too-long
        """
        Python 2 only: Return a view on the values of the original dictionary
        in iteration order.

        See
        `Dictionary View Objects on Python 2 <https://docs.python.org/2/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.viewvalues()

    def viewitems(self):
        # pylint: disable=line-too-long
        """
        Python 2 only: Return a view on the items of the original dictionary
        in iteration order, where each item is a tuple of its key and its value.

        See
        `Dictionary View Objects on Python 2 <https://docs.python.org/2/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.viewitems()

    def __iter__(self):
        """
        Return an iterator through the keys of the original dictionary in
        iteration order.
        """
        return self._dict.__iter__()

    # Other stuff

    def __repr__(self):
        """
        Return a string representation of the original dictionary that is
        suitable for debugging.
        """
        items = ["{0!r}: {1!r}".format(key, value)
                 for key, value in six.iteritems(self)]
        items_str = ', '.join(items)
        return "{0.__class__.__name__}({{{1}}})".format(self, items_str)

    def copy(self):
        """
        Return a shallow copy of the original dictionary.
        """
        org_class = self._dict.__class__
        return org_class(self._dict)

    def __hash__(self):
        """
        Return a hash value for the original dictionary.

        This will raise an exception if the original dictionary is not hashable.
        """
        return self._dict.__hash__()

    def __eq__(self, other):
        """
        Return a boolean indicating whether the original dictionary and the
        other dictionary are equal.
        """
        if isinstance(other, DictView):
            other_dict = other._dict
        else:
            other_dict = other
        return self._dict == other_dict

    def __ne__(self, other):
        """
        Return a boolean indicating whether the original dictionary and the
        other dictionary are not equal.
        """
        return not self.__eq__(other)

    def _raise_ordering_not_supported(self, other, op):
        """
        Function to raise a TypeError indicating that ordering of this class
        is not supported.
        """
        raise TypeError(
            "'{}' not supported between instances of '{}' and '{}'".
            format(op, type(self), type(other)))

    def __lt__(self, other):
        self._raise_ordering_not_supported(other, '<')

    def __gt__(self, other):
        self._raise_ordering_not_supported(other, '>')

    def __ge__(self, other):
        self._raise_ordering_not_supported(other, '>=')

    def __le__(self, other):
        self._raise_ordering_not_supported(other, '<=')


# Remove methods that should only be present in a particular Python version
# If the documentation is built, the methods are not removed in order to show
# them in the documentation.
if six.PY2 and not BUILDING_DOCS:
    del DictView.has_key
    del DictView.iterkeys
    del DictView.itervalues
    del DictView.iteritems
    del DictView.viewkeys
    del DictView.viewvalues
    del DictView.viewitems
