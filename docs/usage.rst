
.. _`Usage`:

Usage
=====


.. _`Supported environments`:

Supported environments
----------------------

The **immutable-views** package is supported in these environments:

* Operating Systems: Linux, macOS / OS-X, native Windows, Linux subsystem in
  Windows, UNIX-like environments in Windows.

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

The following command installs the **immutable-views** package and its
prerequisite packages into the active Python environment:

.. code-block:: bash

    $ pip install immutable-views


.. _`The classes and their usage`:

The classes and their usage
---------------------------

The **immutable-views** package provides collection classes that are immutable
views on other (mutable) collection objects:

* :class:`immutable_views.DictView` - immutable view on another mapping (dictionary) object.
* :class:`immutable_views.ListView` - immutable view on another sequence (list) object.
* :class:`immutable_views.SetView` - immutable view on another set object.

An important behavior of views is that they are "live": Since the view classes
delegate to the underlying collection, any modification of the underlying
collection object will be visible in the view object.

Creating an immutable view on a collection does not copy the collection and
is therefore much faster than creating an immutable copy of the collection.

This is useful if a method or function maintains data in form of a mutable
collection and is intended to return that data but users should not be able to
modify the data. The underlying collection can be updated by the method or
function as needed, but the caller only gets an immutable view on it.

The view classes in the **immutable-views** package implement the complete
behavior of the corresponding Python collection types except for any
operations that would modify the underlying collection object.

The view classes delegate all operations to the underlying collection object
they are a view of. Therefore, the underlying collection can be any kind of
collection implementation (i.e. not just the standard Python collection
classes).

Note that the immutability of the view objects only applies to the view object
itself and to its underlying collection, but not to the items in the underlying
collection. So if the underlying collection contains mutable objects, they will
still be mutable when accessed through the view objects.

Example with dictionaries:

.. code-block:: bash

    $ python
    >>> from immutable_views import DictView
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dictview1 = DictView(dict1)

    # Read-only access to the underlying collection through the view is supported:
    >>> dictview1['a']
    1

    # Modifying the underlying collection through the view is rejected:
    >>> dictview1['a'] = 2
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'DictView' object does not support item assignment

    # Modifications of the underlying collection are visible in the view:
    >>> dict1['a'] = 2
    >>> dictview1['a']
    2

Example with lists:

.. code-block:: bash

    $ python
    >>> from immutable_views import ListView
    >>> list1 = ['a', 'b']
    >>> listview1 = ListView(list1)

    # Read-only access to the underlying collection through the view is supported:
    >>> listview1[0]
    'a'

    # Modifying the underlying collection through the view is rejected:
    >>> listview1[0] = 'c'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'ListView' object does not support item assignment

    # Modifications of the underlying collection are visible in the view:
    >>> list1[0] = 'c'
    >>> listview1[0]
    'c'

Example with sets:

.. code-block:: bash

    $ python
    >>> from immutable_views import SetView
    >>> set1 = {'a', 'b'}
    >>> setview1 = SetView(set1)

    # Read-only access to the underlying collection through the view is supported:
    >>> 'a' in setview1
    True

    # Modifying the underlying collection through the view is rejected:
    >>> setview1.add('c')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'SetView' object has no attribute 'add'

    # Modifications of the underlying collection are visible in the view:
    >>> set1.add('c')
    >>> 'c' in setview1
    True

Note that there are several packages on Pypi that provide immutable
collections, but they all are collections on their own, and not views on
other collections. Here is a notable subset of such packages:

* `immutables <https://pypi.org/project/immutables/>`_
* `pyimmutable <https://pypi.org/project/pyimmutable/>`_
* `frozenordereddict <https://pypi.org/project/frozenordereddict/>`_
* `immutabledict <https://pypi.org/project/immutabledict/>`_
* `frozendict <https://pypi.org/project/immutabledict/>`_
* `itypes <https://pypi.org/project/itypes/>`_
* `HashableDict <https://pypi.org/project/HashableDict/>`_
* `shoobx.immutable <https://pypi.org/project/shoobx.immutable/>`_
* `immutable-collection <https://pypi.org/project/immutable-collection/>`_
* `Dict-Path-Immutable <https://pypi.org/project/Dict-Path-Immutable/>`_
