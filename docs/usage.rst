.. # Licensed under the Apache License, Version 2.0 (the "License");
.. # you may not use this file except in compliance with the License.
.. # You may obtain a copy of the License at
.. #
.. #    http://www.apache.org/licenses/LICENSE-2.0
.. #
.. # Unless required by applicable law or agreed to in writing, software
.. # distributed under the License is distributed on an "AS IS" BASIS,
.. # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. # See the License for the specific language governing permissions and
.. # limitations under the License.

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


.. _`Overview`:

Overview
--------

The **immutable-views** package provides collection classes that are immutable
views on other (mutable) collection objects:

* :class:`~immutable_views.DictView` - immutable view on another mapping (dictionary) object.
* :class:`~immutable_views.ListView` - immutable view on another sequence (list) object.
* :class:`~immutable_views.SetView` - immutable view on another set object.

An important behavior of views is that they are "live": Since the view classes
delegate to the underlying collection, any modification of the underlying
collection object will be visible in the view object.

Creating an immutable view on a collection does not copy the collection and
is therefore much faster than creating an immutable copy of the collection.

The memory overhead of using immutable views is very small: An object
of any of the view classes in the **immutable-views** package occupies 40 Bytes
(measured in CPython 3.9 on macOS), and because the view object only has a
reference to its underlying collection object, that size is independent of the
number of items in the collection.

The compute overhead is also very small, it is basically an additional function
call to the corresponding function of the underlying collection.

Immutable views are useful if a method or function maintains data in form of a
mutable collection and is intended to return that data but users should not be
able to modify the data. The underlying collection can be updated by the method
or function as needed, but the caller only gets an immutable view on it.

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

The standard Python class
`types.MappingProxyType <https://docs.python.org/3/library/types.html#types.MappingProxyType>`_
serves the same purpose as the
:class:`~immutable_views.DictView`
class but it does not support pickling or hashing and was added only in
Python 3.3.
The ``dictproxy`` class from the
`dictproxyhack <https://pypi.org/project/dictproxyhack/>`_
package on Pypi supports Python 2 and Python 3 and uses Python classes where
available (e.g. ``MappingProxyType`` on Python 3.3 and later, and the internal
``mappingproxy`` class used for ``__dict__`` on CPython) but also does not
support pickling or hashing.
The lack of support for standard dictionary behaviors prevents their use in
cases where the view class is used as a read-only replacement for the standard
dictionary.

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


.. _`Examples`:

Examples
--------

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


.. _`Hashing`:

Hashing
-------

A major motivation for providing immutable collections is the support for
hashing.

The immutable view classes provided by the **immutable-views** package however
are only views on the underlying collection. The hashability of the view depends
on the hashability of the underlying collection: If the underlying collection
is immutable, it is hashable and then the view is also hashable.

The immutable view classes therefore implement a ``__hash__()`` method that
delegates to the hash function of the underlying collection. If a collection
object is hashable, the view object using it will be hashable as well.
Otherwise, :exc:`TypeError` is raised when the :func:`hash` function is
called on the view object.

Some examples:

.. table:: Examples for view hashability
    :widths: 15 30 15

    +------------------------------------+--------------------------------+---------------------+
    | View class                         | Underlying collection class    | View hashability    |
    +====================================+================================+=====================+
    | :class:`~immutable_views.DictView` | :class:`dict` (mutable)        | No                  |
    +------------------------------------+--------------------------------+---------------------+
    | :class:`~immutable_views.ListView` | :class:`list` (mutable)        | No                  |
    +------------------------------------+--------------------------------+---------------------+
    | :class:`~immutable_views.ListView` | :class:`tuple` (immutable)     | Yes                 |
    +------------------------------------+--------------------------------+---------------------+
    | :class:`~immutable_views.SetView`  | :class:`set` (mutable)         | No                  |
    +------------------------------------+--------------------------------+---------------------+
    | :class:`~immutable_views.SetView`  | :class:`frozenset` (immutable) | Yes                 |
    +------------------------------------+--------------------------------+---------------------+
