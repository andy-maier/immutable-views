"""
An immutable set view.
"""

from __future__ import print_function, absolute_import

import sys
try:
    from collections.abc import Set
except ImportError:
    # Python 2
    from collections import Set

__all__ = ['SetView']

if sys.version_info[0] == 2:
    # pylint: disable=undefined-variable
    _INTEGER_TYPES = (long, int)  # noqa: F821
else:
    _INTEGER_TYPES = (int,)


class SetView(Set):
    """
    An immutable set view.

    Derived from :class:`~py3:collections.abc.Set`.

    This class provides an immutable view on a possibly mutable set object.
    The set object must be an instance of :class:`~py3:collections.abc.Set`.

    This can be used for example when a class maintains a set that should be
    made available to users of the class without allowing them to modify the
    set.

    In the description of this class, the term 'view' always refers to the
    :class:`SetView` object, and the term 'set' or 'original set' refers to the
    set object the view is based on.

    The :class:`SetView` class supports the complete behavior of Python class
    :class:`set`, except for any methods that would modify the set.
    Note that the non-modifying methods of class :class:`set` are a superset of
    the methods defined for the abstract class :class:`~py3:collections.abc.Set`
    (the methods are listed in the table at the top of the linked page).

    The view is "live": Since the view class delegates all operations to the
    original set, any modification of the original set object will be visible
    in the view object.

    Note that only the view object is immutable, not necessarily its items.
    So if the items in the original set are mutable objects, they can be
    modified through the view.
    """

    def __init__(self, a_set):
        """
        Parameters:

          a_set (:class:`~py3:collections.abc.Set`):
            The original set.
        """
        if not isinstance(a_set, Set):
            raise TypeError(
                "The a_set parameter must be a Set, but is: {}".
                format(type(a_set)))
        self._set = a_set

    def __repr__(self):
        """
        ``repr(self)``:
        Return a string representation of the view suitable for debugging.

        The original set is represented using its ``repr()`` representation.
        """
        return "{0.__class__.__name__}({1!r})".format(self, self._set)

    def __len__(self):
        """
        ``len(self)``:
        Return the number of items in the set.

        The return value is the number of items in the original set.
        """
        return len(self._set)

    def __contains__(self, value):
        """
        ``value in self``:
        Return a boolean indicating whether the set contains a value.

        The return value indicates whether the original set contains an item
        that is equal to the value.
        """
        return value in self._set

    def __iter__(self):
        """
        ``iter(self) ...``:
        Return an iterator through the set.

        The returned iterator yields the items in the original set in its
        iteration order.
        """
        return iter(self._set)

    def __and__(self, other):
        """
        ``self & other``:
        Return a new view on the intersection of the set and the other set.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the left hand operand that contains the items that are in
        the original set of the left hand operand and in the other set
        (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        new_set = self._set & other_set
        return SetView(new_set)

    def __rand__(self, other):
        """
        ``other & self``:
        Return a new view on the intersection of the set and the other set.

        This method is a fallback and is called only if the left operand does
        not support the operation.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the right hand operand that contains the items that are in
        the original set of the right hand operand and in the other set
        (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        return self.__and__(other)

    def intersection(self, *others):
        """
        Return a new view on the intersection of the set and the other
        iterables.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the original set that contains the items that are in the
        original set and in the other iterables (or in case of SetView objects,
        their original sets).

        The other objects must be :term:`iterables <py3:iterable>`.

        The set and the other iterables are not changed.

        Raises:
          TypeError: The other objects are not all iterables.
        """
        # pylint: disable=protected-access
        other_sets = [other._set if isinstance(other, SetView) else other
                      for other in others]
        new_set = self._set.intersection(other_sets)
        return SetView(new_set)

    def __sub__(self, other):
        """
        ``self - other``:
        Return a new view on the difference of the set and the other set.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the left hand operand that contains the items that are in
        the original set of the left hand operand but not in the other set
        (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        new_set = self._set - other_set
        return SetView(new_set)

    def __rsub__(self, other):
        """
        ``other - self``: Not implemented; the other set will need to implement
        :meth:`~py3:object.__sub__()`.

        Raises:
          NotImplementedError
        """
        raise NotImplementedError

    def difference(self, *others):
        """
        Return a new view on the difference of the set and the other
        iterables.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the original set that contains the items that are in the
        original set but not in any of the other iterables (or in case of
        SetView objects, their original sets).

        The other objects must be :term:`iterables <py3:iterable>`.

        The set and the other iterables are not changed.

        Raises:
          TypeError: The other objects are not all iterables.
        """
        # pylint: disable=protected-access
        other_sets = [other._set if isinstance(other, SetView) else other
                      for other in others]
        new_set = self._set.difference(other_sets)
        return SetView(new_set)

    def __or__(self, other):
        """
        ``self | other``:
        Return a new view on the union of the set and the other set.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the left hand operand that contains all the (unique) items
        from the original set of the left hand operand and the other set
        (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        new_set = self._set | other_set
        return SetView(new_set)

    def __ror__(self, other):
        """
        ``other | self``:
        Return a new view on the union of the set and the other set.

        This method is a fallback and is called only if the left operand does
        not support the operation.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the right hand operand that contains all the (unique) items
        from the original set of the right hand operand and the other set
        (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        return self.__or__(other)

    def union(self, *others):
        """
        Return a new view on the union of the set and the other iterables.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the original set that contains all the (unique) items from
        the original set and the other iterables (or in case of SetView objects,
        their original sets).

        The other objects must be :term:`iterables <py3:iterable>`.

        The set and the other iterables are not changed.

        Raises:
          TypeError: The other objects are not all iterables.
        """
        # pylint: disable=protected-access
        other_sets = [other._set if isinstance(other, SetView) else other
                      for other in others]
        new_set = self._set.difference(other_sets)
        return SetView(new_set)

    def __xor__(self, other):
        """
        ``self ^ other``:
        Return a new view on the symmetric difference of the set and the other
        set.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the left hand operand that contains the items that are in
        either the original set of the left hand operand or in the other set
        (or in case of a SetView, its original set), but not in both.

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        new_set = self._set ^ other_set
        return SetView(new_set)

    def __rxor__(self, other):
        """
        ``other ^ self``:
        Return a new view on the symmetric difference of the set and the other
        set.

        This method is a fallback and is called only if the left operand does
        not support the operation.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the right hand operand that contains the items that are in
        either the original set of the right hand operand or in the other set
        (or in case of a SetView, its original set), but not in both.

        The other object must be a :class:`set` or :class:`SetView`.

        The set and the other set are not changed.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        return self.__xor__(other)

    def symmetric_difference(self, other):
        """
        Return a new view on the symmetric difference of the set and the other
        iterable.

        The returned :class:`SetView` object is a view on a new set object of
        the type of the original set that contains the items that are in either
        the original set or in the other iterable (or in case of a SetView, its
        original set), but not in both.

        The other object must be an :term:`py3:iterable`.

        The set and the other iterable are not changed.

        Raises:
          TypeError: The other object is not an iterable.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        new_set = self._set.symmetric_difference(other_set)
        return SetView(new_set)

    def __eq__(self, other):
        """
        ``self == other``:
        Return a boolean indicating whether the set is equal to the other set.

        The return value indicates whether the items in the original set are
        equal to the items in the other set (or in case of a SetView, its
        original set).

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set == other_set

    def __ne__(self, other):
        """
        ``self != other``:
        Return a boolean indicating whether the set is not equal to the other
        set.

        The return value indicates whether the items in the original set are
        not equal to the items in the other set (or in case of a SetView, its
        original set).

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set != other_set

    def __gt__(self, other):
        """
        ``self > other``:
        Return a boolean indicating whether the set is a proper superset of the
        other set.

        The return value indicates whether the original set is a proper
        superset of the other set (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set > other_set

    def __lt__(self, other):
        """
        ``self < other``:
        Return a boolean indicating whether the set is a proper subset of the
        other set.

        The return value indicates whether the original set is a proper
        subset of the other set (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set < other_set

    def __ge__(self, other):
        """
        ``self >= other``:
        Return a boolean indicating whether the set is an inclusive superset
        of the other set.

        The return value indicates whether every element in the other set
        (or in case of a SetView, its original set) is in the original set.

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set >= other_set

    def issuperset(self, other):
        """
        Return a boolean indicating whether the set is an inclusive superset
        of the other iterable.

        The return value indicates whether every element in the other iterable
        (or in case of a SetView, its original set) is in the original set.

        The other object must be an :term:`py3:iterable`.

        Raises:
          TypeError: The other object is not an iterable.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set.issuperset(other_set)

    def __le__(self, other):
        """
        ``self <= other``:
        Return a boolean indicating whether the set is an inclusive subset
        of the other set.

        The return value indicates whether every element in the original
        set is in the other set (or in case of a SetView, its original set).

        The other object must be a :class:`set` or :class:`SetView`.

        Raises:
          TypeError: The other object is not a set or SetView.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set <= other_set

    def issubset(self, other):
        """
        Return a boolean indicating whether the set is an inclusive subset
        of the other iterable.

        The return value indicates whether every element in the original set
        is in the other iterable (or in case of a SetView, its original set).

        The other object must be an :term:`py3:iterable`.

        Raises:
          TypeError: The other object is not an iterable.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set.issubset(other_set)

    def isdisjoint(self, other):
        """
        Return a boolean indicating whether the set does not intersect with
        the other iterable.

        The return value indicates whether the original set has no items in
        common with the other iterable (or in case of a SetView, its original
        set).

        The other object must be an :term:`py3:iterable`.

        Raises:
          TypeError: The other object is not an iterable.
        """
        # pylint: disable=protected-access
        other_set = other._set if isinstance(other, SetView) else other
        return self._set.isdisjoint(other_set)

    def copy(self):
        """
        Return a new view on a shallow copy of the set.

        Note: If the original set is immutable, the new set may be the
        original set object; this is the case e.g. for an empty tuple.
        If the original set is mutable, the new set is always a different
        object than the original set.
        """
        org_class = self._set.__class__
        new_set = org_class(self._set)  # May be same object if immutable
        return SetView(new_set)
