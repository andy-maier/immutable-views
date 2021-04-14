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

.. _`Change log`:

Change log
==========


Version 0.6.0.dev1
------------------

Released: not yet

**Incompatible changes:**

**Deprecations:**

**Bug fixes:**

* Docs: Fixed description of DictView rich comparison methods. (issue #20)

* Docs: Fixed development status of Pypi package to be Beta.

* Fixed that there is no '__reversed__()' method on dict before Python 3.8.

**Enhancements:**

* Removed dependency to 'six' package.

* Stated the memory and compute overhead of using immutable view classes.

* Added support for hashing, dependent on the hashability of the underlying
  collection. (issue #30)

* Added OR (|) operator for DictView on Python 3.9. (issue #38)

* Added tests for pickling DictView. (issue #47)

* Added access to the underlying collections via a property.

* The view classes now use slots for the underlying collection.
  This improves performance and reduces the view object memory size from 48
  Bytes to 40 Bytes. (issue #51)

**Cleanup:**

* Docs: Simplified the introduction section.

* Docs: Removed INSTALL.md file to avoid duplicate information that can become
  inconsistent.

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/andy-maier/immutable-views/issues


Version 0.5.0
-------------

Released: 2021-04-12

Initial release
