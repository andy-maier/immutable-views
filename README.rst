immutable-views - Immutable views on other collection objects
=============================================================

.. image:: https://badge.fury.io/py/immutable-views.svg
    :target: https://pypi.python.org/pypi/immutable-views/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/immutable-views/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/immutable-views/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/immutable-views/badge/?version=latest
    :target: https://readthedocs.org/projects/immutable-views/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/immutable-views/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/immutable-views?branch=master
    :alt: Test coverage (master)


Overview
--------

The **immutable-views** package provides collection classes that are immutable
views on other (mutable) collection objects:

* `immutable_views.DictView <https://immutable-views.readthedocs.io/en/latest/api_dict_view.html>`_ -
  immutable view on another mapping object.
* `immutable_views.ListView <https://immutable-views.readthedocs.io/en/latest/api_list_view.html>`_ -
  immutable view on another list (sequence) object.
* `immutable_views.SetView <https://immutable-views.readthedocs.io/en/latest/api_set_view.html>`_ -
  immutable view on another set object.

An important behavior of views is that they are "live": Since the view
classes delegate to the original collection, any modification of the original
collection object will be visible in the view object.

Creating an immutable view on a collection does not copy the collection and
is therefore much faster than creating an immutable copy of the collection.

This is useful if a method or function maintains data in form of a mutable
collection and is intended to return that data but users should not be able to
modify the data. The original collection can be updated by the method or
function as needed, but the caller only gets an immutable view on it.

The view classes in the **immutable-views** package implement the complete
behavior of the corresponding Python collection types except for any
operations that would modify the collection object.

The view classes delegate all operations to the original collection object they
are a view of. Therefore, the original collection can be any kind of collection
implementation (i.e. not just the original Python collection classes).

Note that the immutability of the view objects only applies to the view object
itself, but not to the items shown by the view. So if the original collection
contains mutable objects, they will still be mutable when accessed through
the view objects. However, since string types are immutable in Python, for
example the common case of a dictionary with string-typed keys and string-typed
values results in complete immutability of the dictionary and its items.

Example with dictionaries:

.. code-block:: bash

    $ python
    >>> from immutable_views import DictView
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dictview1 = DictView(dict1)

    # Read-only access to the view is supported:
    >>> dictview1['a']
    1

    # Modifying the view is rejected:
    >>> dictview1['a'] = 2
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'DictView' object does not support item assignment

    # Modifications of the original collection are visible in the view:
    >>> dict1['a'] = 2
    >>> dictview1['a']
    2

Example with lists:

.. code-block:: bash

    $ python
    >>> from immutable_views import ListView
    >>> list1 = ['a', 'b']
    >>> listview1 = ListView(list1)

    # Read-only access to the view is supported:
    >>> listview1[0]
    'a'

    # Modifying the view is rejected:
    >>> listview1[0] = 'c'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'ListView' object does not support item assignment

    # Modifications of the original collection are visible in the view:
    >>> list1[0] = 'c'
    >>> listview1[0]
    'c'

Example with sets:

.. code-block:: bash

    $ python
    >>> from immutable_views import SetView
    >>> set1 = {'a', 'b'}
    >>> setview1 = SetView(set1)

    # Read-only access to the view is supported:
    >>> 'a' in setview1
    True

    # Modifying the view is rejected:
    >>> setview1.add('c')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'SetView' object has no attribute 'add'

    # Modifications of the original collection are visible in the view:
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


.. _`Documentation and change log`:

Documentation and change log
----------------------------

* `Documentation`_
* `Change log`_


License
-------

The **immutable-views** project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/immutable-views/master/LICENSE>`_.


.. # Links:

.. _`Documentation`: https://immutable-views.readthedocs.io/en/stable/
.. _`Change log`: https://immutable-views.readthedocs.io/en/stable/changes.html
