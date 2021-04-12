"""
An immutable list view.
"""

from __future__ import print_function, absolute_import

try:
    from collections.abc import Sequence
except ImportError:
    # Python 2
    from collections import Sequence

__all__ = ['ListView']


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
    in a new ListView object on a new list object.
    """  # noqa: E501
    # pylint: enable=line-too-long

    def __init__(self, a_list):
        """
        Parameters:

          a_list (:class:`~py3:collections.abc.Sequence`):
            The original list.
            If this object is a ListView, its original list is used.
        """
        if not isinstance(a_list, Sequence):
            raise TypeError(
                "The a_list parameter must be a Sequence, but is: {}".
                format(type(a_list)))
        if isinstance(a_list, ListView):
            a_list = a_list._list
        self._list = a_list

    def __repr__(self):
        """
        ``repr(self)``:
        Return a string representation of the view suitable for debugging.

        The original list is represented using its ``repr()``
        representation.
        """
        return "{0.__class__.__name__}({1!r})".format(self, self._list)

    def __getitem__(self, index):
        """
        ``self[index]``:
         Return the list value at the index position.

        Raises:
          IndexError: Index out of range.
        """
        return self._list[index]

    def __len__(self):
        """
        ``len(self)``:
        Return the number of items in the list.

        The return value is the number of items in the original list.
        """
        return len(self._list)

    def __contains__(self, value):
        """
        ``value in self``:
        Return a boolean indicating whether the list contains a value.

        The return value indicates whether the original list contains an
        item that is equal to the value.
        """
        return value in self._list

    def __iter__(self):
        """
        Return an iterator through the list items.
        """
        return iter(self._list)

    def __add__(self, other):
        """
        ``self + other``:
        Return a new view on the concatenation of the list and the other list.

        The returned :class:`ListView` object is a view on a new list object of
        the type of the left hand operand that contains the items that are in
        the original list of the left hand operand, concatenated with the
        items in the other list (or in case of a ListView, its original list).

        The other object must be an :term:`py3:iterable` or :class:`ListView`.

        The list and the other list are not changed.

        Raises:
          TypeError: The other object is not an iterable.
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        new_list = self._list + other_list
        return ListView(new_list)

    def __mul__(self, number):
        """
        ``self * number``:
        Return a new view on the multiplication of the list with a number.

        The returned :class:`ListView` object is a view on a new list object of
        the type of the left hand operand that contains the items that are in
        the original list of the left hand operand as many times as specified
        by the right hand operand.

        A number <= 0 causes the returned list to be empty.

        The left hand operand is not changed.
        """
        new_list = self._list * number
        return ListView(new_list)

    def __rmul__(self, number):
        """
        ``number * self``:
        Return a new view on the multiplication of the list with a number.

        This method is a fallback and is called only if the left operand does
        not support the operation.

        The returned :class:`ListView` object is a view on a new list object of
        the type of the right hand operand that contains the items that are in
        the original list of the right hand operand as many times as specified
        by the left hand operand.

        A number <= 0 causes the returned list to be empty.

        The right hand operand is not changed.
        """
        return self * number  # Delegates to __mul__()

    def __reversed__(self):
        """
        ``reversed(self) ...``:
        Return an iterator through the list in reversed iteration order.

        The returned iterator yields the items in the original list in the
        reversed iteration order.
        """
        return reversed(self._list)

    def __eq__(self, other):
        """
        ``self == other``:
        Return a boolean indicating whether the list is equal to the other list.

        The return value indicates whether the items in the original list are
        equal to the items in the other list (or in case of a ListView, its
        original list).

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list == other_list

    def __ne__(self, other):
        """
        ``self != other``:
        Return a boolean indicating whether the list is not equal to the other
        list.

        The return value indicates whether the items in the original list are
        not equal to the items in the other list (or in case of a ListView, its
        original list).

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list != other_list

    def __gt__(self, other):
        # pylint: disable=line-too-long
        """
        ``self > other``:
        Return a boolean indicating whether the list is greater than the other
        list.

        The return value indicates whether the original list is greater than
        the other list (or in case of a ListView, its original list), based on
        the lexicographical ordering Python defines for sequence types
        (see https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """  # noqa: E501
        # pylint: enable=line-too-long
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list > other_list

    def __lt__(self, other):
        # pylint: disable=line-too-long
        """
        ``self < other``:
        Return a boolean indicating whether the list is less than the other
        list.

        The return value indicates whether the original list is less than
        the other list (or in case of a ListView, its original list), based on
        the lexicographical ordering Python defines for sequence types
        (see https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """  # noqa: E501
        # pylint: enable=line-too-long
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list < other_list

    def __ge__(self, other):
        # pylint: disable=line-too-long
        """
        ``self < other``:
        Return a boolean indicating whether the list is greater than or equal to
        the other list.

        The return value indicates whether the original list is greater than or
        equal to the other list (or in case of a ListView, its original list),
        based on the lexicographical ordering Python defines for sequence types
        (see https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """  # noqa: E501
        # pylint: enable=line-too-long
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list >= other_list

    def __le__(self, other):
        # pylint: disable=line-too-long
        """
        ``self < other``:
        Return a boolean indicating whether the list is less than or equal to
        the other list.

        The return value indicates whether the original list is less than or
        equal to the other list (or in case of a ListView, its original list),
        based on the lexicographical ordering Python defines for sequence types
        (see https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)

        The other object must be a :class:`list` or :class:`ListView`.

        Raises:
          TypeError: The other object is not a list or ListView.
        """  # noqa: E501
        # pylint: enable=line-too-long
        # pylint: disable=protected-access
        other_list = other._list if isinstance(other, ListView) else other
        return self._list <= other_list

    def count(self, value):
        """
        Return the number of times the specified value occurs in the list.
        """
        return self._list.count(value)

    def copy(self):
        """
        Return a new view on a shallow copy of the list.

        The returned :class:`ListView` object is a new view object on a list
        object of the type of the original list.

        If the list type is immutable, the returned list object may be the
        original list object. If the list type is mutable, the returned list is
        a new list object that is a shallow copy of the original list object.
        """
        org_class = self._list.__class__
        new_list = org_class(self._list)  # May be same object if immutable
        return ListView(new_list)

    def index(self, value, start=0, stop=9223372036854775807):
        """
        Return the index of the first item in the list with the specified value.

        The search is limited to the index range defined by the specified
        ``start`` and ``stop`` parameters, whereby ``stop`` is the index
        of the first item after the search range.

        Raises:
          ValueError: No such item is found.
        """
        return self._list.index(value, start, stop)
