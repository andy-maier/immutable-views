"""
An immutable dictionary view.
"""

from __future__ import print_function, absolute_import

import os
try:
    from collections.abc import Mapping
except ImportError:
    # Python 2
    from collections import Mapping
import six

__all__ = ['DictView']

# This env var is set when building the docs. It causes the methods
# that are supposed to exist only in a particular Python version, not to be
# removed, so they appear in the docs.
BUILDING_DOCS = os.environ.get('BUILDING_DOCS', False)


class DictView(Mapping):
    # pylint: disable=line-too-long
    """
    An immutable dictionary view.

    Derived from :class:`~py3:collections.abc.Mapping`.

    This class provides an immutable view on a possibly mutable mapping
    object. The mapping object must be an instance of
    :class:`~py3:collections.abc.Mapping`, e.g. :class:`dict`, or a
    user-defined class.

    This can be used for example when a class maintains a dictionary that should
    be made available to users of the class without allowing them to modify the
    dictionary.

    In the description of this class, the term 'view' always refers to the
    :class:`DictView` object, and the term 'dictionary' or
    'underlying dictionary' refers to the mapping object the view is based on.

    The :class:`DictView` class supports the complete behavior of Python class
    :class:`dict`, except for any methods that would modify the dictionary.
    Note that the non-modifying methods of class :class:`dict` are a superset of
    the methods defined for the abstract class
    :class:`~py3:collections.abc.Mapping` (the methods are listed in the table
    at the top of the linked page).

    The view is "live": Since the view class delegates all operations to the
    underlying dictionary, any modification of the underlying dictionary object
    will be visible in the view object.

    Note that only the view object is immutable, not its items. So if the values
    in the underlying dictionary are mutable objects, they can be modified
    through the view.

    Note that in Python, augmented assignment (e.g. ``x += y``) is not
    guaranteed to modify the left hand object in place, but can result in the
    left hand name being bound to a new object (like in ``x = x + y``).
    For details, see
    `object.__iadd__() <https://docs.python.org/3/reference/datamodel.html#object.__iadd__>`_.

    For the DictView class, augmented assignment is supported and results in
    binding the left hand name to a new DictView object.
    """  # noqa: E501
    # pylint: enable=line-too-long

    def __init__(self, a_dict):
        """
        Parameters:

          a_dict (:class:`~py3:collections.abc.Mapping`):
            The underlying dictionary.
            If this object is a DictView, its underlying dictionary is used.
        """
        if not isinstance(a_dict, Mapping):
            raise TypeError(
                "The a_dict parameter must be a Mapping, but is: {}".
                format(type(a_dict)))
        if isinstance(a_dict, DictView):
            a_dict = a_dict._dict
        self._dict = a_dict

    def __repr__(self):
        """
        ``repr(self)``:
        Return a string representation of the view suitable for debugging.

        The underlying dictionary is represented using its ``repr()``
        representation.
        """
        return "{0.__class__.__name__}({1!r})".format(self, self._dict)

    def __getitem__(self, key):
        """
        ``self[key]``:
        Return the value of the dictionary item with an existing key.

        Raises:
          KeyError: Key does not exist.
        """
        return self._dict[key]

    def __len__(self):
        """
        ``len(self)``:
        Return the number of items in the dictionary.

        The return value is the number of items in the underlying dictionary.
        """
        return len(self._dict)

    def __contains__(self, key):
        """
        ``value in self``:
        Return a boolean indicating whether the dictionary contains a value.

        The return value indicates whether the underlying dictionary contains an
        item that is equal to the value.
        """
        return key in self._dict

    def __reversed__(self):
        """
        ``reversed(self) ...``:
        Return an iterator through the dictionary in reversed iteration order.

        The returned iterator yields the items in the underlying dictionary in
        the reversed iteration order.
        """
        return reversed(self._dict)

    def get(self, key, default=None):
        """
        Return the value of the dictionary item with an existing key or a
        default value.
        """
        return self._dict.get(key, default)

    def has_key(self, key):
        """
        Python 2 only: Return a boolean indicating whether the dictionary
        contains an item with the key.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.has_key(key)  # noqa: W601

    # Iteration methods

    def keys(self):
        # pylint: disable=line-too-long
        """
        Return the dictionary keys.

        The keys of the underlying dictionary are returned in iteration order
        and as a view in Python 3 and as a list in Python 2.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.keys()

    def values(self):
        # pylint: disable=line-too-long
        """
        Return the dictionary values.

        The values of the underlying dictionary are returned in iteration order
        and as a view in Python 3 and as a list in Python 2.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.values()

    def items(self):
        # pylint: disable=line-too-long
        """
        Return the dictionary items.

        The items of the underlying dictionary are returned in iteration order
        and as a view in Python 3 and as a list in Python 2.
        Each returned item is a tuple of key and value.

        See
        `Dictionary View Objects on Python 3 <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.items()

    def iterkeys(self):
        """
        Python 2 only: Return an iterator through the dictionary keys.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.iterkeys()

    def itervalues(self):
        """
        Python 2 only: Return an iterator through the dictionary values.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.itervalues()

    def iteritems(self):
        """
        Python 2 only: Return an iterator through the dictionary items.
        Each item is a tuple of key and value.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """
        return self._dict.iteritems()

    def viewkeys(self):
        # pylint: disable=line-too-long
        """
        Python 2 only: Return a view on the dictionary keys.

        The keys of the underlying dictionary are returned in iteration order
        and as a view.

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
        Python 2 only: Return a view on the dictionary values.

        The values of the underlying dictionary are returned in iteration order
        and as a view.

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
        Python 2 only: Return a view on the dictionary items.

        The items of the underlying dictionary are returned in iteration order
        and as a view. Each returned item is a tuple of key and value.

        See
        `Dictionary View Objects on Python 2 <https://docs.python.org/2/library/stdtypes.html#dictionary-view-objects>`_ for details about view objects.

        Raises:
          AttributeError: The method does not exist on Python 3.
        """  # noqa: E501
        # pylint: enable=line-too-long
        return self._dict.viewitems()

    def __iter__(self):
        """
        Return an iterator through the dictionary keys.
        """
        return iter(self._dict)

    def copy(self):
        """
        Return a new view on a shallow copy of the dictionary.

        The returned :class:`DictView` object is a new view object on a
        dictionary object of the type of the underlying dictionary.

        If the dictionary type is immutable, the returned dictionary object may
        be the underlying dictionary object. If the dictionary type is mutable,
        the returned dictionary is a new dictionary object that is a shallow
        copy of the underlying dictionary object.
        """
        org_class = self._dict.__class__
        new_dict = org_class(self._dict)  # May be same object if immutable
        return DictView(new_dict)

    def __eq__(self, other):
        """
        ``self == other``:
        Return a boolean indicating whether the dictionary is equal to the
        other dictionary.

        Two dictionaries are equal if and only if all items in the dictionaries
        match by their keys and matching items have equal values.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is not a dict or DictView.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict == other_dict

    def __ne__(self, other):
        """
        ``self != other``:
        Return a boolean indicating whether the dictionary is not equal to the
        other dictionary.

        Two dictionaries are equal if and only if all items in the dictionaries
        match by their keys and matching items have equal values.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is not a dict or DictView.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict != other_dict

    def __gt__(self, other):
        """
        ``self > other``:
        Return a boolean indicating whether the dictionary is greater than
        the other dictionary.

        Whether such an ordering comparison is supported and what it means is
        up to the underlying dictionary and the other dictionary. For example,
        the standard Python :class:`dict` class rejects ordering comparisons
        starting with Python 3.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is not a dict or DictView.
          TypeError: Operator not supported.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict > other_dict

    def __lt__(self, other):
        """
        ``self < other``:
        Return a boolean indicating whether the dictionary is less than
        the other dictionary.

        Whether such an ordering comparison is supported and what it means is
        up to the underlying dictionary and the other dictionary. For example,
        the standard Python :class:`dict` class rejects ordering comparisons
        starting with Python 3.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is dict a set or DictView.
          TypeError: Operator not supported.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict < other_dict

    def __ge__(self, other):
        """
        ``self >= other``:
        Return a boolean indicating whether the dictionary is greater than or
        equal to the other dictionary.

        Whether such an ordering comparison is supported and what it means is
        up to the underlying dictionary and the other dictionary. For example,
        the standard Python :class:`dict` class rejects ordering comparisons
        starting with Python 3.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is not a dict or DictView.
          TypeError: Operator not supported.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict >= other_dict

    def __le__(self, other):
        """
        ``self <= other``:
        Return a boolean indicating whether the dictionary is less than or
        equal to the other dictionary.

        Whether such an ordering comparison is supported and what it means is
        up to the underlying dictionary and the other dictionary. For example,
        the standard Python :class:`dict` class rejects ordering comparisons
        starting with Python 3.

        The other object must be a :class:`dict` or :class:`DictView`.

        Raises:
          TypeError: The other object is not a dict or DictView.
          TypeError: Operator not supported.
        """
        # pylint: disable=protected-access
        other_dict = other._dict if isinstance(other, DictView) else other
        return self._dict <= other_dict


# Remove methods that should only be present in a particular Python version
# If the documentation is built, the methods are not removed in order to show
# them in the documentation.
if not six.PY2 and not BUILDING_DOCS:
    del DictView.has_key
    del DictView.iterkeys
    del DictView.itervalues
    del DictView.iteritems
    del DictView.viewkeys
    del DictView.viewvalues
    del DictView.viewitems
