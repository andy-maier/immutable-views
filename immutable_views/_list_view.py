"""
An immutable list view.
"""

from __future__ import print_function, absolute_import

import sys
try:
    from collections.abc import Sequence
except ImportError:
    # Python 2
    from collections import Sequence

__all__ = ['ListView']

if sys.version_info[0] == 2:
    # pylint: disable=undefined-variable
    _INTEGER_TYPES = (long, int)  # noqa: F821
else:
    _INTEGER_TYPES = (int,)


class ListView(Sequence):
    # pylint: disable=line-too-long
    """
    An immutable list view.

    Derived from :class:`~py3:collections.abc.Sequence`.

    This is an immutable view on an original (mutable)
    :class:`~py3:collections.abc.Sequence` object, e.g. :class:`list` or
    :class:`tuple`.

    The view class supports the complete Python list behavior, except for
    any operations that would modify the list. More precisely, the view
    class supports all methods of :class:`~py3:collections.abc.Sequence`
    (the methods are listed in the table at the top of the linked page).

    The view is "live": Since the view class delegates all operations to the
    original list, any modification of the original list object
    will be visible in the view object.

    Note that only the view object is immutable, not its items. So if the values
    in the original list are mutable objects, they can be modified through the
    view.

    Note that in Python, augmented assignment (e.g. `+=` is not guaranteed to
    modify the left hand object in place, but can result in a new object.
    For details, see
    `object.__iadd__() <https://docs.python.org/3/reference/datamodel.html#object.__iadd__>`_.
    The `+=` operator on a left hand object that is a ListView object results
    in a new ListView object on a new original list object.
    """  # noqa: E501

    # Methods not implemented:
    #
    # * __getattribute__(self, name): The method inherited from object is used;
    #   no reason to have a different implementation.

    def __init__(self, a_list):
        """
        Parameters:

          a_list (:class:`~py3:collections.abc.Sequence`):
            The original list.
        """
        if not isinstance(a_list, Sequence):
            raise TypeError(
                "The a_list parameter must be a Sequence, but is: {}".
                format(type(a_list)))
        self._list = a_list

    def __repr__(self):
        """
        Return a string representation of the original list that is
        suitable for debugging.
        """
        return "{0.__class__.__name__}({1!r})".format(self, self._list)

    def __getitem__(self, index):
        """
        Return the value in the original list at the index position.
        """
        return self._list[index]

    def __len__(self):
        """
        Return the number of items in the original list.
        """
        return len(self._list)

    def __contains__(self, value):
        """
        Return a boolean indicating whether the list contains at least one
        item with the value.
        """
        return value in self._list

    def __iter__(self):
        """
        Return an iterator through the original list in iteration order.
        """
        return iter(self._list)

    def __add__(self, other):
        """
        Return a new :class:`ListView` object that is a view on a new list
        object that contains the items from the left hand operand (``self``)
        and the items from the right hand operand (``other``).

        The operands are not changed.

        Raises:
          TypeError: The other iterable is not an iterable
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        new_list = self._list + other_list
        return ListView(new_list)

    def __mul__(self, number):
        """
        Return a new :class:`ListView` object that is a view on a new list
        object that contains the items from the left hand operand (``self``)
        as many times as specified by the right hand operand (``number``).

        A number <= 0 causes the returned list to be empty.

        The operands are not changed.
        """
        new_list = self._list * number
        return ListView(new_list)

    def __rmul__(self, number):
        """
        Return a new :class:`ListView` object that is a view on a new list
        object that contains the items from the right hand operand (``self``)
        as many times as specified by the left hand operand (``number``).

        A number <= 0 causes the returned list to be empty.

        The right hand operand (``self``) is not changed.
        """
        return self * number  # Delegates to __mul__()

    def __reversed__(self):
        """
        Return a new :class:`ListView` object that is a view on a new list
        object that that is a shallow copy of the list that has its items
        reversed in order.
        """
        new_list = list(reversed(self._list))
        return ListView(new_list)

    def __eq__(self, other):
        """
        Return a boolean indicating whether the original list is
        equal to
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list == other_list

    def __ne__(self, other):
        """
        Return a boolean indicating whether the original list is
        not equal to
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list != other_list

    def __gt__(self, other):
        """
        Return a boolean indicating whether the original list is
        greater than
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list > other_list

    def __lt__(self, other):
        """
        Return a boolean indicating whether the original list is
        less than
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list < other_list

    def __ge__(self, other):
        """
        Return a boolean indicating whether the original list is
        greater than or equal to
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list >= other_list

    def __le__(self, other):
        """
        Return a boolean indicating whether the original list is
        less than or equal to
        the other list (or in case of a ListView, its original list).
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list <= other_list

    def count(self, value):
        """
        Return the number of times the specified value occurs in the
        original list.
        """
        return self._list.count(value)

    def copy(self):
        """
        Return a new ListView object that is a view on a new list that
        is a shallow copy of the original list.

        Note: If the original list is immutable, the new list may be the
        original list object; this is the case e.g. for an empty tuple.
        If the original list is mutable, the new list is always a different
        object than the original list.
        """
        org_class = self._list.__class__
        new_list = org_class(self._list)  # May be same object if immutable
        return ListView(new_list)

    def index(self, value, start=0, stop=9223372036854775807):
        """
        Return the index of the first item that is equal to the specified
        value.

        The search is limited to the index range defined by the specified
        ``start`` and ``stop`` parameters, whereby ``stop`` is the index
        of the first item after the search range.

        Raises:
          ValueError: No such item is found.
        """
        return self._list.index(value, start, stop)
