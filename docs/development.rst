
.. _`Development`:

Development
===========

This section only needs to be read by developers of the
immutable-views project,
including people who want to make a fix or want to test the project.


.. _`Repository`:

Repository
----------

The repository for the immutable-views project is on GitHub:

https://github.com/andy-maier/immutable-views


.. _`Setting up the development environment`:

Setting up the development environment
--------------------------------------

1. If you have write access to the Git repo of this project, clone it using
   its SSH link, and switch to its working directory:

   .. code-block:: bash

        $ git clone git@github.com:andy-maier/immutable-views.git
        $ cd immutable-views

   If you do not have write access, create a fork on GitHub and clone the
   fork in the way shown above.

2. It is recommended that you set up a `virtual Python environment`_.
   Have the virtual Python environment active for all remaining steps.

3. Install the project for development.
   This will install Python packages into the active Python environment,
   and OS-level packages:

   .. code-block:: bash

        $ make develop

4. This project uses Make to do things in the currently active Python
   environment. The command:

   .. code-block:: bash

        $ make

   displays a list of valid Make targets and a short description of what each
   target does.

.. _virtual Python environment: https://docs.python-guide.org/en/latest/dev/virtualenvs/


.. _`Building the documentation`:

Building the documentation
--------------------------

The ReadTheDocs (RTD) site is used to publish the documentation for the
project package at https://immutable-views.readthedocs.io/

This page is automatically updated whenever the Git repo for this package
changes the branch from which this documentation is built.

In order to build the documentation locally from the Git work directory,
execute:

.. code-block:: bash

    $ make builddoc

The top-level document to open with a web browser will be
``build_doc/html/docs/index.html``.


.. _`Testing`:

.. # Keep the tests/README file in sync with this 'Testing' section.

Testing
-------


All of the following `make` commands run the tests in the currently active
Python environment.
Depending on how the `immutable-views` package is installed in
that Python environment, either the directories in the main repository
directory are used, or the installed package.
The test case files and any utility functions they use are always used from
the `tests` directory in the main repository directory.

The `tests` directory has the following subdirectory structure:

::

    tests
     +-- unittest            Unit tests

There are multiple types of tests:

1. Unit tests

   These tests can be run standalone, and the tests validate their results
   automatically.

   They are run by executing:

   .. code-block:: bash

       $ make test

   Test execution can be modified by a number of environment variables, as
   documented in the make help (execute `make help`).

   An alternative that does not depend on the makefile and thus can be executed
   from the source distribution archive, is:

   .. code-block:: bash

       $ ./setup.py test

   Options for pytest can be passed using the ``--pytest-options`` option.


To run the unit tests in all supported Python environments, the
Tox tool can be used. It creates the necessary virtual Python environments and
executes `make test` (i.e. the unit tests) in each of them.

For running Tox, it does not matter which Python environment is currently
active, as long as the Python `tox` package is installed in it:

.. code-block:: bash

    $ tox                              # Run tests on all supported Python versions
    $ tox -e py27                      # Run tests on Python 2.7


.. _`Testing from the source archives on Pypi or GitHub`:

Testing from the source archives on Pypi or GitHub
--------------------------------------------------

The wheel distribution archives on Pypi (e.g. ``*.whl``) contain only the
files needed to run this package, but not the files needed to test it.

The source distribution archives on Pypi and GitHub (e.g. ``*.tar.gz``)
contain all files that are needed to run and to test this package. This allows
testing the package without having to check out the entire repository, and is
convenient for testing e.g. when packaging into OS-level packages.
Nevertheless, the test files are not installed when installing these source
distribution archives.

The following commands download the source distribution archive on Pypi for a
particular version of the package into the current directory and unpack it:

.. code-block:: bash

    $ pip download --no-deps --no-binary :all: immutable-views==1.0.0
    $ tar -xf immutable-views-1.0.0.tar.gz
    $ cd immutable-views-1.0.0
    $ ls -1
    -rw-r--r--   1 johndoe  staff    468 Jun 29 22:31 INSTALL.md
    -rw-r--r--   1 johndoe  staff  26436 May 26 06:45 LICENSE.txt
    -rw-r--r--   1 johndoe  staff    367 Jul  3 07:54 MANIFEST.in
    -rw-r--r--   1 johndoe  staff   3451 Jul  3 07:55 PKG-INFO
    -rw-r--r--   1 johndoe  staff   7665 Jul  2 23:20 README.rst
    drwxr-xr-x  29 johndoe  staff    928 Jul  3 07:55 immutable-views
    drwxr-xr-x   8 johndoe  staff    256 Jul  3 07:55 immutable-views.egg-info
    -rw-r--r--   1 johndoe  staff   1067 Jun 29 22:31 requirements.txt
    -rw-r--r--   1 johndoe  staff     38 Jul  3 07:55 setup.cfg
    -rwxr-xr-x   1 johndoe  staff   7555 Jul  3 07:24 setup.py
    -rw-r--r--   1 johndoe  staff   2337 Jul  2 23:20 test-requirements.txt
    drwxr-xr-x  15 johndoe  staff    480 Jul  3 07:55 tests

This package, its dependent packages for running it, and its dependent packages
for testing it can be installed with the package extra named "test":

.. code-block:: bash

    $ pip install .[test]

When testing in Linux distributions that include this package as an OS-level
package, the corresponding OS-level packages would instead be installed for
these dependent Python packages. The ``test-requirements.txt`` file shows which
dependent Python packages are needed for testing this package.

Finally, the tests can be run using the ``setup.py`` script:

.. code-block:: bash

    $ ./setup.py test

These commands are listed in the help of the ``setup.py`` script:

.. code-block:: bash

    $ ./setup.py --help-commands

    . . .

    Extra commands:
      . . .
      test              Run unit tests using pytest
      . . .

The additional options supported by these commands are shown in their help:

.. code-block:: bash

    $ ./setup.py test --help

    . . .

    Options for 'test' command:
      --pytest-options  additional options for pytest, as one argument

    . . .

Note: The ``test`` command of ``setup.py`` is not the deprecated built-in
command (see `<https://github.com/pypa/setuptools/issues/1684>`_), but has been
implemented in ``setup.py`` in such a way that it only runs the tests but
does not install anything upfront.
Therefore, this approach can be used for testing in Linux distributions that
include this package as an OS-level package.


.. _`Contributing`:

Contributing
------------

Third party contributions to this project are welcome!

In order to contribute, create a `Git pull request`_, considering this:

.. _Git pull request: https://help.github.com/articles/using-pull-requests/

* Test is required.
* Each commit should only contain one "logical" change.
* A "logical" change should be put into one commit, and not split over multiple
  commits.
* Large new features should be split into stages.
* The commit message should not only summarize what you have done, but explain
  why the change is useful.

What comprises a "logical" change is subject to sound judgement. Sometimes, it
makes sense to produce a set of commits for a feature (even if not large).
For example, a first commit may introduce a (presumably) compatible API change
without exploitation of that feature. With only this commit applied, it should
be demonstrable that everything is still working as before. The next commit may
be the exploitation of the feature in other components.

For further discussion of good and bad practices regarding commits, see:

* `OpenStack Git Commit Good Practice`_

* `How to Get Your Change Into the Linux Kernel`_

.. _OpenStack Git Commit Good Practice: https://wiki.openstack.org/wiki/GitCommitMessages
.. _How to Get Your Change Into the Linux Kernel: https://www.kernel.org/doc/Documentation/SubmittingPatches

Further rules:

* The following long-lived branches exist and should be used as targets for
  pull requests:

  - ``master`` - for next functional version

  - ``stable_$MN`` - for fix stream of released version M.N.

* We use topic branches for everything!

  - Based upon the intended long-lived branch, if no dependencies

  - Based upon an earlier topic branch, in case of dependencies

  - It is valid to rebase topic branches and force-push them.

* We use pull requests to review the branches.

  - Use the correct long-lived branch (e.g. ``master`` or ``stable_0.2``) as a
    merge target.

  - Review happens as comments on the pull requests.

  - At least one approval is required for merging.

* GitHub meanwhile offers different ways to merge pull requests. We merge pull
  requests by rebasing the commit from the pull request.

Releasing a version to PyPI
---------------------------

This section describes how to release a version of immutable-views
to PyPI.

It covers all variants of versions that can be released:

* Releasing a new major version (Mnew.0.0) based on the master branch
* Releasing a new minor version (M.Nnew.0) based on the master branch
* Releasing a new update version (M.N.Unew) based on the stable branch of its
  minor version

The description assumes that the `andy-maier/immutable-views`
Github repo is cloned locally and its upstream repo is assumed to have the Git
remote name `origin`.

Any commands in the following steps are executed in the main directory of your
local clone of the `andy-maier/immutable-views`
Git repo.

1.  Set shell variables for the version that is being released and the branch
    it is based on:

    * ``MNU`` - Full version M.N.U that is being released
    * ``MN`` - Major and minor version M.N of that full version
    * ``BRANCH`` - Name of the branch the version that is being released is
      based on

    When releasing a new major version (e.g. ``1.0.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=1.0.0
        MN=1.0
        BRANCH=master

    When releasing a new minor version (e.g. ``0.9.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=0.9.0
        MN=0.9
        BRANCH=master

    When releasing a new update version (e.g. ``0.8.1``) based on the stable
    branch of its minor version:

    .. code-block:: sh

        MNU=0.8.1
        MN=0.8
        BRANCH=stable_${MN}

2.  Create a topic branch for the version that is being released:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git checkout -b release_${MNU}

3.  Edit the version file:

    .. code-block:: sh

        vi immutable-views/_version.py

    and set the ``__version__`` variable to the version that is being released:

    .. code-block:: python

        __version__ = 'M.N.U'

4.  Edit the change log:

    .. code-block:: sh

        vi docs/changes.rst

    and make the following changes in the section of the version that is being
    released:

    * Finalize the version.
    * Change the release date to today's date.
    * Make sure that all changes are described.
    * Make sure the items shown in the change log are relevant for and
      understandable by users.
    * In the "Known issues" list item, remove the link to the issue tracker and
      add text for any known issues you want users to know about.
    * Remove all empty list items.

5.  When releasing based on the master branch, edit the GitHub workflow file
    ``test.yml``:

    .. code-block:: sh

        vi .github/workflows/test.yml

    and in the ``on`` section, increase the version of the ``stable_*`` branch
    to the new stable branch ``stable_M.N`` created earlier:

    .. code-block:: yaml

        on:
          schedule:
            . . .
          push:
            branches: [ master, stable_M.N ]
          pull_request:
            branches: [ master, stable_M.N ]

6.  Commit your changes and push the topic branch to the remote repo:

    .. code-block:: sh

        git status  # Double check the changed files
        git commit -asm "Release ${MNU}"
        git push --set-upstream origin release_${MNU}

7.  On GitHub, create a Pull Request for branch ``release_M.N.U``. This will
    trigger the CI runs.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When releasing based on a stable branch, you need to
    change the target branch of the Pull Request to ``stable_M.N``.

8.  On GitHub, close milestone ``M.N.U``.

9.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

10. Add a new tag for the version that is being released and push it to
    the remote repo. Clean up the local repo:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git tag -f ${MNU}
        git push -f --tags
        git branch -d release_${MNU}

11. When releasing based on the master branch, create and push a new stable
    branch for the same minor version:

    .. code-block:: sh

        git checkout -b stable_${MN}
        git push --set-upstream origin stable_${MN}
        git checkout ${BRANCH}

    Note that no GitHub Pull Request is created for any ``stable_*`` branch.

12. On GitHub, edit the new tag ``M.N.U``, and create a release description on
    it. This will cause it to appear in the Release tab.

    You can see the tags in GitHub via Code -> Releases -> Tags.

13. On ReadTheDocs, activate the new version ``M.N.U``:

    * Go to https://readthedocs.org/projects/immutable-views/versions/
      and log in.

    * Activate the new version ``M.N.U``.

      This triggers a build of that version. Verify that the build succeeds
      and that new version is shown in the version selection popup at
      https://immutable-views.readthedocs.io/

14. Upload the package to PyPI:

    .. code-block:: sh

        make upload

    This will show the package version and will ask for confirmation.

    **Attention!** This only works once for each version. You cannot release
    the same version twice to PyPI.

    Verify that the released version arrived on PyPI at
    https://pypi.python.org/pypi/immutable-views/


Starting a new version
----------------------

This section shows the steps for starting development of a new version of the
immutable-views project in its Git repo.

This section covers all variants of new versions:

* Starting a new major version (Mnew.0.0) based on the master branch
* Starting a new minor version (M.Nnew.0) based on the master branch
* Starting a new update version (M.N.Unew) based on the stable branch of its
  minor version

The description assumes that the `andy-maier/immutable-views`
Github repo is cloned locally and its upstream repo is assumed to have the Git
remote name `origin`.

Any commands in the following steps are executed in the main directory of your
local clone of the `andy-maier/immutable-views`
Git repo.

1.  Set shell variables for the version that is being started and the branch it
    is based on:

    * ``MNU`` - Full version M.N.U that is being started
    * ``MN`` - Major and minor version M.N of that full version
    * ``BRANCH`` -  Name of the branch the version that is being started is
      based on

    When starting a new major version (e.g. ``1.0.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=1.0.0
        MN=1.0
        BRANCH=master

    When starting a new minor version (e.g. ``0.9.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=0.9.0
        MN=0.9
        BRANCH=master

    When starting a new minor version (e.g. ``0.8.1``) based on the stable
    branch of its minor version:

    .. code-block:: sh

        MNU=0.8.1
        MN=0.8
        BRANCH=stable_${MN}

2.  Create a topic branch for the version that is being started:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git checkout -b start_${MNU}

3.  Edit the version file:

    .. code-block:: sh

        vi immutable-views/_version.py

    and update the version to a draft version of the version that is being
    started:

    .. code-block:: python

        __version__ = 'M.N.U.dev1'

4.  Edit the change log:

    .. code-block:: sh

        vi docs/changes.rst

    and insert the following section before the top-most section:

    .. code-block:: rst

        immutable-views M.N.U.dev1
        ---------------------

        Released: not yet

        **Incompatible changes:**

        **Deprecations:**

        **Bug fixes:**

        **Enhancements:**

        **Cleanup:**

        **Known issues:**

        * See `list of open issues`_.

        .. _`list of open issues`: https://github.com/andy-maier/immutable-views/issues

5.  Commit your changes and push them to the remote repo:

    .. code-block:: sh

        git status  # Double check the changed files
        git commit -asm "Start ${MNU}"
        git push --set-upstream origin start_${MNU}

6.  On GitHub, create a Pull Request for branch ``start_M.N.U``.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When starting a version based on a stable branch, you
    need to change the target branch of the Pull Request to ``stable_M.N``.

7.  On GitHub, create a milestone for the new version ``M.N.U``.

    You can create a milestone in GitHub via Issues -> Milestones -> New
    Milestone.

8.  On GitHub, go through all open issues and pull requests that still have
    milestones for previous releases set, and either set them to the new
    milestone, or to have no milestone.

9.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

10. Update and clean up the local repo:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git branch -d start_${MNU}
