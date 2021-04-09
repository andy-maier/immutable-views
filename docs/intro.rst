
.. _`Introduction`:

Introduction
============

The **immutable-views** package provides collection classes that are immutable
views on other (mutable) collection objects:

* :class:`immutable_views.DictView` - immutable view on another dict (mapping) object.
* :class:`immutable_views.ListView` - immutable view on another list (sequence) object.
* :class:`immutable_views.SetView` - immutable view on another set object.

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
    TypeError: 'SetView' object does not support item assignment

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


.. _`Installation`:

Installation
------------


.. _`Supported environments`:

Supported environments
^^^^^^^^^^^^^^^^^^^^^^

The package does not have any dependencies on the type of operating system and
is regularly tested in CI systems on the following operating systems:

* Ubuntu, native Windows, CygWin, OS-X / macOS

The package is supported on the following Python versions:

* Python: 2.7, 3.4 and all higher 3.x versions


.. _`Installing`:

Installing
^^^^^^^^^^

* Prerequisites:

  - The Python environment into which you want to install must be the current
    Python environment, and must have at least the following Python packages
    installed:

    - setuptools
    - wheel
    - pip

* Install the immutable-views package and its prerequisite
  Python packages into the active Python environment:

  .. code-block:: bash

      $ pip install immutable-views


.. _`Installing a different version`:

Installing a different version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The examples in the previous sections install the latest version of
immutable-views that is released on `PyPI`_.
This section describes how different versions of immutable-views
can be installed.

* To install an older released version of immutable-views,
  Pip supports specifying a version requirement. The following example installs
  immutable-views version 0.1.0
  from PyPI:

  .. code-block:: bash

      $ pip install immutable-views==0.1.0

* If you need to get a certain new functionality or a new fix that is
  not yet part of a version released to PyPI, Pip supports installation from a
  Git repository. The following example installs immutable-views
  from the current code level in the master branch of the
  `immutable-views repository`_:

  .. code-block:: bash

      $ pip install git+https://github.com/andy-maier/immutable-views.git@master#egg=immutable-views

.. _immutable-views repository: https://github.com/andy-maier/immutable-views

.. _PyPI: https://pypi.python.org/pypi


.. _`Verifying the installation`:

Verifying the installation
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can verify that immutable-views is installed correctly by
importing the package into Python (using the Python environment you installed
it to):

.. code-block:: bash

    $ python -c "import immutable-views; print('ok')"
    ok


.. _`Compatibility and deprecation policy`:

Compatibility and deprecation policy
------------------------------------

The immutable-views project uses the rules of
`Semantic Versioning 2.0.0`_ for compatibility between versions, and for
deprecations. The public interface that is subject to the semantic versioning
rules and specificically to its compatibility rules are the APIs and commands
described in this documentation.

.. _Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html

The semantic versioning rules require backwards compatibility for new minor
versions (the 'N' in version 'M.N.P') and for new patch versions (the 'P' in
version 'M.N.P').

Thus, a user of an API or command of the immutable-views project
can safely upgrade to a new minor or patch version of the
immutable-views package without encountering compatibility
issues for their code using the APIs or for their scripts using the commands.

In the rare case that exceptions from this rule are needed, they will be
documented in the :ref:`Change log`.

Occasionally functionality needs to be retired, because it is flawed and a
better but incompatible replacement has emerged. In the
immutable-views project, such changes are done by deprecating
existing functionality, without removing it immediately.

The deprecated functionality is still supported at least throughout new minor
or patch releases within the same major release. Eventually, a new major
release may break compatibility by removing deprecated functionality.

Any changes at the APIs or commands that do introduce
incompatibilities as defined above, are described in the :ref:`Change log`.

Deprecation of functionality at the APIs or commands is
communicated to the users in multiple ways:

* It is described in the documentation of the API or command

* It is mentioned in the change log.

* It is raised at runtime by issuing Python warnings of type
  ``DeprecationWarning`` (see the Python :mod:`py:warnings` module).

Since Python 2.7, ``DeprecationWarning`` messages are suppressed by default.
They can be shown for example in any of these ways:

* By specifying the Python command line option: ``-W default``
* By invoking Python with the environment variable: ``PYTHONWARNINGS=default``

It is recommended that users of the immutable-views project
run their test code with ``DeprecationWarning`` messages being shown, so they
become aware of any use of deprecated functionality.

Here is a summary of the deprecation and compatibility policy used by
the immutable-views project, by version type:

* New patch version (M.N.P -> M.N.P+1): No new deprecations; no new
  functionality; backwards compatible.
* New minor release (M.N.P -> M.N+1.0): New deprecations may be added;
  functionality may be extended; backwards compatible.
* New major release (M.N.P -> M+1.0.0): Deprecated functionality may get
  removed; functionality may be extended or changed; backwards compatibility
  may be broken.


.. _'Python namespaces`:

Python namespaces
-----------------

This documentation describes only the external APIs of the
immutable-views project, and omits any internal symbols and
any sub-modules.
