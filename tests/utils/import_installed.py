"""
import_installed - Utility function for testing the installed version of the
package.
"""

from __future__ import absolute_import, print_function

import sys
import os

__all__ = ['import_installed']


def import_installed(module_name):
    """
    Import a Python module/package, controlling whether it is loaded from the
    normal Python module search path, or from an installed version (excluding
    the module in the current directory).

    The TEST_INSTALLED environment variable controls this as follows:

      * If not set or empty, the normal Python module search path is used.
        Because that search path contains the current directory in front of the
        list, this will cause a module directory in the current directory to
        have precedence over any installed versions of the module.

      * If non-empty, the current directory is removed from the Python module
        search path, and an installed version of the module is thus used, even
        when a module directory exists in the current directory. This can be
        used for testing an OS-installed version of the module.

    Example usage, e.g. in a test program::

        from ...utils import import_installed
        xyz = import_installed('xyz')  # pylint: disable=invalid-name
        from xyz import ...

    The number of dots in `from ..utils` depends on where the test program
    containing this code is located, relative to the tests/utils.py file.
    """
    test_installed = os.getenv('TEST_INSTALLED')
    if test_installed:

        # Remove '' directory.
        dirpath = ''
        try:
            ix = sys.path.index(dirpath)
        except ValueError:
            ix = None
        if ix is not None:
            if test_installed == 'DEBUG':
                print("Debug: Removing {0} at index {1} from module search "
                      "path".format(dirpath, ix))
            del sys.path[ix]

        # Move CWD to end. Reason is that when testing with an editable
        # installation, the CWD is needed, but when testing with a non-editable
        # installation, the package should not be found inthe CWD.
        # Note that somehow the CWD gets inserted at the begin of the search
        # path every time, so we need a loop.
        dirpath = os.getcwd()
        while True:
            try:
                ix = sys.path.index(dirpath)
            except ValueError:
                if test_installed == 'DEBUG':
                    print("Debug: Appending {0} to end of module search "
                          "path".format(dirpath))
                sys.path.append(dirpath)
                break
            if ix == len(sys.path) - 1:
                # it exists once at the end
                break
            if test_installed == 'DEBUG':
                print("Debug: Removing {0} at index {1} from module search "
                      "path".format(dirpath, ix))
            del sys.path[ix]

    if module_name not in sys.modules:
        module = __import__(module_name, level=0)  # only absolute imports
        if test_installed == 'DEBUG':
            print("Debug: {0} module newly loaded from: {1}".
                  format(module_name, module.__file__))
    else:
        module = sys.modules[module_name]
        if test_installed == 'DEBUG':
            print("Debug: {0} module was already loaded from: {1}".
                  format(module_name, module.__file__))
    return module
