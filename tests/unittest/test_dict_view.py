# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test the DictView class.
"""

from __future__ import absolute_import

import sys
import re
import pickle
from collections import OrderedDict
try:
    from collections.abc import KeysView, ValuesView, ItemsView, Iterator, \
        MutableMapping, Mapping
except ImportError:
    from collections import KeysView, ValuesView, ItemsView, Iterator, \
        MutableMapping, Mapping
import pytest
from nocasedict import NocaseDict, HashableMixin

from ..utils.simplified_test_function import simplified_test_function

# pylint: disable=wrong-import-position, wrong-import-order, invalid-name
from ..utils.import_installed import import_installed
immutable_views = import_installed('immutable_views')
from immutable_views import DictView  # noqa: E402
# pylint: enable=wrong-import-position, wrong-import-order, invalid-name


class HashableDict(HashableMixin, NocaseDict):
    """Hashable dictionary, for testing"""
    pass


class NorDict(Mapping):
    """Dictionary without OR operator, for testing"""

    def __init__(self, a_dict=None):
        if a_dict is None:
            a_dict = {}
        self._dict = dict(a_dict)

    def __getitem__(self, key):
        return self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)


class OrDict(NorDict):
    """Dictionary with OR operator, for testing"""

    def __or__(self, other):
        return self._dict | dict(other)

    def __ror__(self, other):
        return dict(other) | self._dict


class DerivedDict(dict):
    """Dictionary derived from dict with additional attribute"""

    def __init__(self, *args, **kwargs):
        super(DerivedDict, self).__init__(*args, **kwargs)
        self._dummy = 'dummy'

    def __eq__(self, other):
        super_equal = super(DerivedDict, self).__eq__(other)
        if isinstance(other, DerivedDict):
            return super_equal and self._dummy == other._dummy
        return super_equal


class DerivedDictView(DictView):
    """Dictionary view derived from DictView with additional attribute"""

    def __init__(self, *args, **kwargs):
        super(DerivedDictView, self).__init__(*args, **kwargs)
        self._dummy = 'dummy'

    def __eq__(self, other):
        super_equal = super(DerivedDictView, self).__eq__(other)
        if isinstance(other, DerivedDictView):
            return super_equal and self._dummy == other._dummy
        return super_equal


PY2 = sys.version_info[0] == 2

# Indicates Python dict supports lt/gt comparison (between dicts)
DICT_SUPPORTS_COMPARISON = sys.version_info[0:2] == (2, 7)

# Indicates Python dict is ordered
DICT_IS_ORDERED = sys.version_info[0:2] >= (3, 7)

# Indicates Python dict issues UserWarning about not preserving order
# of items in kwargs or in standard dict
DICT_WARNS_ORDER = sys.version_info[0:2] <= (3, 6)

# Indicates Python dict supports the iter..() and view..() methods
DICT_SUPPORTS_ITER_VIEW = sys.version_info[0:2] == (2, 7)

# Indicates Python dict supports the has_key() method
DICT_SUPPORTS_HAS_KEY = sys.version_info[0:2] == (2, 7)

# Indicates Python dict supports the __reversed__() method
DICT_SUPPORTS_REVERSED = sys.version_info[0:2] >= (3, 8)

# Indicates Python dict supports the __or__/__ror__() methods
DICT_SUPPORTS_OR = sys.version_info[0:2] >= (3, 9)

# Used as indicator not to pass an argument in the testcases.
# Note this has nothing to do with the _OMITTED flag in _immutable_views.py and
# could be a different value.
_OMIT_ARG = object()


class NonEquatable(object):
    # pylint: disable=too-few-public-methods
    """
    Class that raises TypeError when comparing its objects for equality.
    """

    def __eq__(self, other):
        raise TypeError("Cannot compare %s to %s" % (type(self), type(other)))

    def __ne__(self, other):
        raise TypeError("Cannot compare %s to %s" % (type(self), type(other)))


TESTCASES_DICTVIEW_INIT = [

    # Testcases for DictView.__init__() / ncd=DictView()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to DictView().
    #   * init_kwargs: Dict of keyword arguments to DictView().
    #   * exp_dict: Expected resulting dictionary, as OrderedDict.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty underlying dictionaries
    (
        "From empty dict as positional arg",
        dict(
            init_args=({},),
            init_kwargs={},
            exp_dict=DictView({}),
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "From empty OrderedDict as positional arg",
        dict(
            init_args=(OrderedDict(),),
            init_kwargs={},
            exp_dict=DictView(OrderedDict()),
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "From DictView of empty dict as positional arg",
        dict(
            init_args=(DictView({}),),
            init_kwargs={},
            exp_dict=DictView({}),
            verify_order=True,
        ),
        None, None, True
    ),

    # Non-empty underlying dictionaries
    (
        "From non-empty dict as positional arg",
        dict(
            init_args=({'Dog': 'Cat', 'Budgie': 'Fish'},),
            init_kwargs={},
            exp_dict=DictView({'Dog': 'Cat', 'Budgie': 'Fish'}),
            verify_order=False,
        ),
        None, None, True
    ),
    (
        "From DictView of non-empty dict as positional arg",
        dict(
            init_args=(DictView({'Dog': 'Cat', 'Budgie': 'Fish'}),),
            init_kwargs={},
            exp_dict=DictView({'Dog': 'Cat', 'Budgie': 'Fish'}),
            verify_order=False,
        ),
        None, None, True
    ),

    # Error cases with inputs that are invalid for the view but would be valid
    # for a real dictionary
    (
        "From no args (a_dict parameter required)",
        dict(
            init_args=(),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From None as positional arg (Must be Mapping type)",
        dict(
            init_args=(None,),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From empty list as positional arg (Must be Mapping type)",
        dict(
            init_args=(list(),),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From empty tuple as positional arg (Must be Mapping type)",
        dict(
            init_args=(tuple(),),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From list as positional arg (Must be Mapping type)",
        dict(
            init_args=([('Dog', 'Cat'), ('Budgie', 'Fish')],),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From tuple as positional arg (Must be Mapping type)",
        dict(
            init_args=((('Dog', 'Cat'), ('Budgie', 'Fish')),),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From keyword args (Must be Mapping type)",
        dict(
            init_args=(),
            init_kwargs={'Dog': 'Cat', 'Budgie': 'Fish'},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From list as positional arg and keyword args (Must be Mapping type)",
        dict(
            init_args=([('Dog', 'Cat')],),
            init_kwargs={'Budgie': 'Fish'},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From tuple as positional arg and keyword args (Must be Mapping type)",
        dict(
            init_args=((('Dog', 'Cat'),),),
            init_kwargs={'Budgie': 'Fish'},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "From dict as positional arg and keyword args (Must be Mapping type)",
        dict(
            init_args=({'Dog': 'Cat'},),
            init_kwargs={'Budgie': 'Fish'},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),

    # Other error cases
    (
        "String as positional arg (Must be Mapping type)",
        dict(
            init_args=('illegal',),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Integer as positional arg (Must be Mapping type)",
        dict(
            init_args=(42,),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Two positional args (too many args)",
        dict(
            init_args=(list(), list()),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "List as positional arg, whose item has only one item "
        "(Must be Mapping type)",
        dict(
            init_args=([('Dog',)],),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "List as positional arg, whose item has too many items "
        "(Must be Mapping type)",
        dict(
            init_args=([('Dog', 'Cat', 'bad')],),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Tuple as positional arg, whose item has only one item "
        "(Must be Mapping type)",
        dict(
            init_args=((('Dog',),),),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Tuple as positional arg, whose item has too many items "
        "(Must be Mapping type)",
        dict(
            init_args=((('Dog', 'Cat', 'bad'),),),
            init_kwargs={},
            exp_dict=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_INIT)
@simplified_test_function
def test_DictView_init(
        testcase, init_args, init_kwargs, exp_dict, verify_order):
    """
    Test function for DictView.__init__() / ncd=DictView()
    """

    # The code to be tested
    act_dict = DictView(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # The verification below also uses some DictView features, but that is
    # unavoidable if we want to work through the public interface:

    act_items = []
    for key in act_dict:  # Uses DictView iteration
        act_value = act_dict[key]  # Uses DictView getitem
        assert key in exp_dict, "Unexpected extra key %r" % key
        exp_value = exp_dict[key]
        assert act_value == exp_value, "Unexpected value at key %r" % key
        act_items.append((key, act_value))

    exp_items = []
    for key in exp_dict:
        exp_value = exp_dict[key]
        # Next line uses DictView contains:
        assert key in act_dict, "Unexpected missing key %r" % key
        act_value = act_dict[key]  # Uses DictView getitem
        assert act_value == exp_value, "Unexpected value at key %r" % key
        exp_items.append((key, exp_value))

    if verify_order:
        assert act_items == exp_items, "Unexpected order of items"


TESTCASES_DICTVIEW_GETITEM = [

    # Testcases for DictView.__getitem__() / ncd[key]

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * key: Key to be used for the test.
    #   * exp_value: Expected value for the key.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty underlying dictionary
    (
        "Empty underlying dict, with None key (not found)",
        dict(
            obj=DictView({}),
            key=None,
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Empty underlying dict, with integer key (not found)",
        dict(
            obj=DictView({}),
            key=1234,
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Empty underlying dict, with empty string key (not found)",
        dict(
            obj=DictView({}),
            key='',
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Empty underlying dict, with non-empty key (not found)",
        dict(
            obj=DictView({}),
            key='Dog',
            exp_value=None,
        ),
        KeyError, None, True
    ),

    # Non-empty underlying dictionary
    (
        "Non-empty underlying dict, with None key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key=None,
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Non-empty underlying dict, with empty string key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='',
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Non-empty underlying dict, with non-existing key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='invalid',
            exp_value=None,
        ),
        KeyError, None, True
    ),
    (
        "Non-empty underlying dict, with existing key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='Dog',
            exp_value='Cat',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_GETITEM)
@simplified_test_function
def test_DictView_getitem(testcase, obj, key, exp_value):
    """
    Test function for DictView.__getitem__() / ncd[key]
    """

    # The code to be tested
    act_value = obj[key]

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_value == exp_value, "Unexpected value at key %r" % key


TESTCASES_DICTVIEW_LEN = [

    # Testcases for DictView.__len__() / len(ncd)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * exp_len: Expected len() value.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dict",
        dict(
            obj=DictView({}),
            exp_len=0,
        ),
        None, None, True
    ),
    (
        "Dict with two items",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            exp_len=2,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_LEN)
@simplified_test_function
def test_DictView_len(testcase, obj, exp_len):
    """
    Test function for DictView.__len__() / len(ncd)
    """

    # The code to be tested
    act_len = len(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_len == exp_len


TESTCASES_DICTVIEW_CONTAINS = [

    # Testcases for DictView.__contains__() / key in ncd

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * key: Key to be used for the test.
    #   * exp_result: Expected result (bool).
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty DictView
    (
        "Empty dict, with None key",
        dict(
            obj=DictView({}),
            key=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty dict, with integer key",
        dict(
            obj=DictView({}),
            key=1234,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty dict, with empty string key (not found)",
        dict(
            obj=DictView({}),
            key='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty dict, with non-empty key (not found)",
        dict(
            obj=DictView({}),
            key='Dog',
            exp_result=False,
        ),
        None, None, True
    ),

    # Non-empty DictView
    (
        "Non-empty dict, with non-existing None key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with empty string key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with non-empty key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='invalid',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with existing key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='Dog',
            exp_result=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_CONTAINS)
@simplified_test_function
def test_DictView_contains(testcase, obj, key, exp_result):
    """
    Test function for DictView.__contains__() / key in ncd
    """

    # The code to be tested
    act_result = key in obj

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result, \
        "Unexpected result at key {k!r}".format(k=key)


TESTCASES_DICTVIEW_HAS_KEY = [

    # Testcases for DictView.has_key()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * key: Key to be used for the test.
    #   * exp_result: Expected result (bool).
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty DictView
    (
        "Empty dict, with None key",
        dict(
            obj=DictView({}),
            key=None,
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Empty dict, with integer key (no lower / success)",
        dict(
            obj=DictView({}),
            key=1234,
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Empty dict, with empty string key (not found)",
        dict(
            obj=DictView({}),
            key='',
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Empty dict, with non-empty key (not found)",
        dict(
            obj=DictView({}),
            key='Dog',
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),

    # Non-empty DictView
    (
        "Non-empty dict, with non-existing None key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key=None,
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Non-empty dict, with empty string key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='',
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Non-empty dict, with non-empty key (not found)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='invalid',
            exp_result=False,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
    (
        "Non-empty dict, with existing key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='Dog',
            exp_result=True,
        ),
        AttributeError if not DICT_SUPPORTS_HAS_KEY else None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_HAS_KEY)
@simplified_test_function
def test_DictView_has_key(testcase, obj, key, exp_result):
    """
    Test function for DictView.has_key()
    """

    # The code to be tested
    act_result = obj.has_key(key)  # noqa: W601

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result, \
        "Unexpected result at key {k!r}".format(k=key)


TESTCASES_DICTVIEW_REVERSED = [

    # Testcases for DictView.__reversed__() / reversed(ncd)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * exp_keys: Expected result as a list of keys, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dict",
        dict(
            obj=DictView({}),
            exp_keys=[],
        ),
        None if DICT_SUPPORTS_REVERSED else TypeError, None, DICT_IS_ORDERED
    ),
    (
        "Dict with one item",
        dict(
            obj=DictView({'Dog': 'Cat'}),
            exp_keys=['Dog'],
        ),
        None if DICT_SUPPORTS_REVERSED else TypeError, None, DICT_IS_ORDERED
    ),
    (
        "Dict with two items",
        dict(
            obj=DictView({'Dog': 'Cat', 'Budgie': 'Fish'}),
            exp_keys=['Budgie', 'Dog'],
        ),
        None if DICT_SUPPORTS_REVERSED else TypeError, None, DICT_IS_ORDERED
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_REVERSED)
@simplified_test_function
def test_DictView_reversed(testcase, obj, exp_keys):
    """
    Test function for DictView.__reversed__() / reversed(ncd)
    """

    # The code to be tested
    act_keys_iter = reversed(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # The reason we verify that an iterator is returned is that
    # DictView.__reversed__() delegates to keys() which returns a list in
    # Python 2, so this verifies that reversed() still turns this into an
    # iterator.
    assert isinstance(act_keys_iter, Iterator)

    act_keys = list(act_keys_iter)
    assert act_keys == exp_keys


TESTCASES_DICTVIEW_GET = [

    # Testcases for DictView.get()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * key: Key to be used for the test.
    #   * default: Default value to be used for the test, or _OMIT_ARG.
    #   * exp_value: Expected value at the key.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty DictView
    (
        "Empty dict, with None key",
        dict(
            obj=DictView({}),
            key=None,
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Empty dict, with integer key",
        dict(
            obj=DictView({}),
            key=1234,
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Empty dict, with empty string key (defaulted without default)",
        dict(
            obj=DictView({}),
            key='',
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Empty dict, with empty string key (defaulted to a value)",
        dict(
            obj=DictView({}),
            key='',
            default='Newbie',
            exp_value='Newbie',
        ),
        None, None, True
    ),
    (
        "Empty dict, with non-empty key (defaulted without default)",
        dict(
            obj=DictView({}),
            key='Dog',
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Empty dict, with non-empty key (defaulted to a value)",
        dict(
            obj=DictView({}),
            key='Dog',
            default='Kitten',
            exp_value='Kitten',
        ),
        None, None, True
    ),

    # Non-empty DictView
    (
        "Non-empty dict, with None key",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key=None,
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with empty string key (defaulted without default)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='',
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with empty string key (defaulted to a value)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='',
            default='Newbie',
            exp_value='Newbie',
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with non-empty non-existing key (defaulted without "
        "default)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='invalid',
            default=_OMIT_ARG,
            exp_value=None,
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with non-empty non-existing key (defaulted to a "
        "value)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='invalid',
            default='Newbie',
            exp_value='Newbie',
        ),
        None, None, True
    ),
    (
        "Non-empty dict, with existing key (no default)",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            key='Dog',
            default=_OMIT_ARG,
            exp_value='Cat',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_GET)
@simplified_test_function
def test_DictView_get(testcase, obj, key, default, exp_value):
    """
    Test function for DictView.get()
    """

    # The code to be tested
    if default is _OMIT_ARG:
        act_value = obj.get(key)
    else:
        act_value = obj.get(key, default)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_value == exp_value, \
        "Unexpected value at key {k!r} with default {d}". \
        format(k=key, d="omitted" if default is _OMIT_ARG else repr(default))


TESTCASES_DICTVIEW_ITEMS = [

    # Testcases for DictView.keys(), values(), items()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    #   * exp_items: List with expected items (key,value) in expected order.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dict",
        dict(
            obj=DictView({}),
            exp_items=[],
        ),
        None, None, True
    ),
    (
        "Dict with one item",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat')])),
            exp_items=[('Dog', 'Cat')],
        ),
        None, None, True
    ),
    (
        "Dict with two items",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
            exp_items=[('Dog', 'Cat'), ('Budgie', 'Fish')],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_keys(testcase, obj, exp_items):
    """
    Test function for DictView.keys()
    """

    # The code to be tested
    act_keys = obj.keys()

    # Also test iterating through the result
    act_keys_list = list(act_keys)

    # Test that second iteration is possible
    act_keys_list2 = list(act_keys)

    if not PY2:

        # Test __contained__() of the returned view
        for key in act_keys_list:
            assert key in act_keys

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if PY2:
        assert isinstance(act_keys, list)
    else:
        assert isinstance(act_keys, KeysView)

    exp_keys = [item[0] for item in exp_items]
    assert act_keys_list == exp_keys
    assert act_keys_list2 == exp_keys


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_values(testcase, obj, exp_items):
    """
    Test function for DictView.values()
    """

    # The code to be tested
    act_values = obj.values()

    # Also test iterating through the result
    act_values_list = list(act_values)

    # Test that second iteration is possible
    act_values_list2 = list(act_values)

    if not PY2:

        # Test __contained__() of the returned view
        for value in act_values_list:
            assert value in act_values

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if PY2:
        assert isinstance(act_values, list)
    else:
        assert isinstance(act_values, ValuesView)

    exp_values = [item[1] for item in exp_items]
    assert act_values_list == exp_values
    assert act_values_list2 == exp_values


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_items(testcase, obj, exp_items):
    """
    Test function for DictView.items()
    """

    # The code to be tested
    act_items = obj.items()

    # Also test iterating through the result
    act_items_list = list(act_items)

    # Test that second iteration is possible
    act_items_list2 = list(act_items)

    if not PY2:

        # Test __contained__() of the returned view
        for item in act_items_list:
            assert item in act_items

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if PY2:
        assert isinstance(act_items, list)
    else:
        assert isinstance(act_items, ItemsView)

    assert act_items_list == exp_items
    assert act_items_list2 == exp_items


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_iterkeys(testcase, obj, exp_items):
    """
    Test function for DictView.iterkeys()
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does not support iterkeys() method")

    assert PY2

    # The code to be tested
    act_keys = []
    for key in obj.iterkeys():
        act_keys.append(key)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    exp_keys = [item[0] for item in exp_items]
    assert act_keys == exp_keys


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_itervalues(testcase, obj, exp_items):
    """
    Test function for DictView.itervalues()
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does not support itervalues() method")

    assert PY2

    # The code to be tested
    act_values = []
    for value in obj.itervalues():
        act_values.append(value)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    exp_values = [item[1] for item in exp_items]
    assert act_values == exp_values


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_iteritems(testcase, obj, exp_items):
    """
    Test function for DictView.iteritemss()
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does not support iteritems() method")

    assert PY2

    # The code to be tested
    act_items = []
    for item in obj.iteritems():
        act_items.append(item)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_items == exp_items


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_viewkeys(testcase, obj, exp_items):
    """
    Test function for DictView.viewkeys() (PY2 only)
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does support viewkeys() method")

    assert PY2

    # The code to be tested
    act_keys = obj.viewkeys()

    # Also test iterating through the result
    act_keys_list = list(act_keys)

    # Test that second iteration is possible
    act_keys_list2 = list(act_keys)

    # Test __contained__() of the returned view
    for key in act_keys_list:
        assert key in act_keys

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(act_keys, KeysView)

    exp_keys = [item[0] for item in exp_items]
    assert act_keys_list == exp_keys
    assert act_keys_list2 == exp_keys


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_viewvalues(testcase, obj, exp_items):
    """
    Test function for DictView.viewvalues()
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does not support viewvalues() method")

    assert PY2

    # The code to be tested
    act_values = obj.viewvalues()

    # Also test iterating through the result
    act_values_list = list(act_values)

    # Test that second iteration is possible
    act_values_list2 = list(act_values)

    # Test __contained__() of the returned view
    for value in act_values_list:
        assert value in act_values

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(act_values, ValuesView)

    exp_values = [item[1] for item in exp_items]
    assert act_values_list == exp_values
    assert act_values_list2 == exp_values


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_viewitems(testcase, obj, exp_items):
    """
    Test function for DictView.viewitems()
    """

    if not DICT_SUPPORTS_ITER_VIEW:
        pytest.skip("Test dictionary does not support viewitems() method")

    assert PY2

    # The code to be tested
    act_items = obj.viewitems()

    # Also test iterating through the result
    act_items_list = list(act_items)

    # Test that second iteration is possible
    act_items_list2 = list(act_items)

    # Test __contained__() of the returned view
    for item in act_items_list:
        assert item in act_items

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(act_items, ItemsView)

    assert act_items_list == exp_items
    assert act_items_list2 == exp_items


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ITEMS)
@simplified_test_function
def test_DictView_iter(testcase, obj, exp_items):
    """
    Test function for DictView.__iter__() / for key in ncd
    """

    # The code to be tested
    act_keys = []
    for key in obj:
        act_keys.append(key)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    exp_keys = [item[0] for item in exp_items]
    assert act_keys == exp_keys


TESTCASES_DICTVIEW_REPR = [

    # Testcases for DictView.__repr__() / repr(ncd)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: DictView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dict",
        dict(
            obj=DictView({}),
        ),
        None, None, True
    ),
    (
        "Dict with two items",
        dict(
            obj=DictView(OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_REPR)
@simplified_test_function
def test_DictView_repr(testcase, obj):
    """
    Test function for DictView.__repr__() / repr(ncd)
    """

    # The code to be tested
    result = repr(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert re.match(r'^DictView\(.*\)$', result)

    # Note: This only tests for existence of each item, not for excess items
    # or representing the correct order.
    for item in obj.items():
        exp_item_result1 = "{0!r}: {1!r}".format(*item)
        exp_item_result2 = "({0!r}, {1!r})".format(*item)
        assert exp_item_result1 in result or exp_item_result2 in result


TESTCASES_DICTVIEW_COPY = [

    # Testcases for DictView.copy()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * dictview: DictView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "DictView with empty dict",
        dict(
            dictview=DictView({}),
        ),
        None, None, True
    ),
    (
        "DictView with dict with two items",
        dict(
            dictview=DictView(
                dict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
        ),
        None, None, True
    ),
    (
        "DictView with OrderedDict with two items",
        dict(
            dictview=DictView(
                OrderedDict([('Dog', 'Cat'), ('Budgie', 'Fish')])),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_COPY)
@simplified_test_function
def test_DictView_copy(testcase, dictview):
    """
    Test function for DictView.copy()
    """

    dictview_dict = dictview.dict

    # The code to be tested
    dictview_copy = dictview.copy()

    dictview_copy_dict = dictview_copy.dict

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the result type
    # pylint: disable=unidiomatic-typecheck
    assert type(dictview_copy) is DictView

    # Verify the result is a different object than the DictView
    assert id(dictview_copy) != id(dictview)

    # Verify the new dictionary is a different object than the underlying
    # dictionary, if mutable
    if isinstance(dictview_dict, MutableMapping):
        assert id(dictview_copy_dict) != id(dictview_dict)

    # Verify the new dictionary has the same type as the underlying dictionary
    # pylint: disable=unidiomatic-typecheck
    assert type(dictview_copy_dict) == type(dictview_dict)

    # Verify the new dictionary is equal to the underlying dictionary
    assert dictview_copy_dict == dictview_dict


TESTCASES_DICTVIEW_EQUAL = [

    # Testcases for DictView.__eq__(), __ne__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: DictView object #1 to use.
    #   * obj2: DictView object #2 to use.
    #   * exp_obj_equal: Expected equality of the objects.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dictionary",
        dict(
            obj1=DictView({}),
            obj2=DictView({}),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "One item, keys and values equal",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1')])),
            obj2=DictView(OrderedDict([('k1', 'v1')])),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "One item, keys equal, values different",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1')])),
            obj2=DictView(OrderedDict([('k1', 'v1_x')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "One item, keys different, values equal",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1')])),
            obj2=DictView(OrderedDict([('k2', 'v1')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "One item, keys equal, values both None",
        dict(
            obj1=DictView(OrderedDict([('k1', None)])),
            obj2=DictView(OrderedDict([('k1', None)])),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two equal items, in same order",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1'), ('k2', 'v2')])),
            obj2=DictView(OrderedDict([('k1', 'v1'), ('k2', 'v2')])),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two equal items in ordered dict, in different order",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1'), ('k2', 'v2')])),
            obj2=DictView(OrderedDict([('k2', 'v2'), ('k1', 'v1')])),
            exp_obj_equal=False,
        ),
        None, None, False
    ),
    (
        "Two equal items in standard dict, in different order",
        dict(
            obj1=DictView(dict([('k1', 'v1'), ('k2', 'v2')])),
            obj2=DictView(dict([('k2', 'v2'), ('k1', 'v1')])),
            exp_obj_equal=not DICT_IS_ORDERED,
        ),
        None, None, False
    ),
    (
        "Comparing unicode value with bytes value",
        dict(
            obj1=DictView(OrderedDict([('k1', b'v1')])),
            obj2=DictView(OrderedDict([('k2', u'v2')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Matching unicode key with string key",
        dict(
            obj1=DictView(OrderedDict([('k1', 'v1')])),
            obj2=DictView(OrderedDict([(u'k2', 'v2')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Higher key missing",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Lower key missing",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Dog', 'Cat')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "First non-matching key is less. But longer size!",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([
                ('Budgie', 'Fish'), ('Curly', 'Snake'), ('Cozy', 'Dog'),
            ])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Only non-matching keys that are less. But longer size!",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict(
                [('Alf', 'F'), ('Anton', 'S'), ('Aussie', 'D')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "First non-matching key is greater. But shorter size!",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgio', 'Fish')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Only non-matching keys that are greater. But shorter size!",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Zoe', 'F')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. First non-matching key is less",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict(
                [('Budgie', 'Fish'), ('Curly', 'Snake')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. Only non-matching keys that are less",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Alf', 'F'), ('Anton', 'S')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. Only non-matching keys that are greater",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Zoe', 'F'), ('Zulu', 'S')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size, only matching keys. First non-matching value is less",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Car')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size, only matching keys. First non-matching value is greater",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Caz')])),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "A value raises TypeError when compared (and equal still succeeds)",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict(
                [('Budgie', NonEquatable()), ('Dog', 'Cat')])),
            exp_obj_equal=False,
        ),
        TypeError, None, True
    ),

    (
        "Mixing types: DictView of dict and dict",
        dict(
            obj1=DictView(dict({'Dog': 'Cat'})),
            obj2=dict({'Dog': 'Cat'}),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Mixing types: dict and DictView of dict",
        dict(
            obj1=dict({'Dog': 'Cat'}),
            obj2=DictView(dict({'Dog': 'Cat'})),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Mixing types: DictView of dict and OrDict (not a dict)",
        dict(
            obj1=DictView(dict({'Dog': 'Cat'})),
            obj2=OrDict({'Dog': 'Cat'}),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Mixing types: dict and DictView of OrDict (not a dict)",
        dict(
            obj1=dict({'Dog': 'Cat'}),
            obj2=DictView(OrDict({'Dog': 'Cat'})),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Mixing types: DictView of OrDict (not a dict) and DictView of dict",
        dict(
            obj1=DictView(OrDict({'Dog': 'Cat'})),
            obj2=DictView(dict({'Dog': 'Cat'})),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Mixing types: DictView of dict and DictView of OrDict (not a dict)",
        dict(
            obj1=DictView(dict({'Dog': 'Cat'})),
            obj2=DictView(OrDict({'Dog': 'Cat'})),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_EQUAL)
@simplified_test_function
def test_DictView_eq(testcase, obj1, obj2, exp_obj_equal):
    """
    Test function for DictView.__eq__() / ncd1==ncd2
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    eq1 = (obj1 == obj2)
    eq2 = (obj2 == obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert eq1 == exp_obj_equal
    assert eq2 == exp_obj_equal


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_EQUAL)
@simplified_test_function
def test_DictView_ne(testcase, obj1, obj2, exp_obj_equal):
    """
    Test function for DictView.__ne__() / ncd1!=ncd2
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    ne1 = (obj1 != obj2)
    ne2 = (obj2 != obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert ne1 != exp_obj_equal
    assert ne2 != exp_obj_equal


TESTCASES_DICTVIEW_ORDERING = [

    # Testcases for DictView.__le__(), __lt__(), __ge__(), __gt__() / ord.ops

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: DictView object #1 to be used.
    #   * obj2: DictView object #2 to be used.
    #   * op: Order comparison operator to be used, as a string (e.g. '>')
    #   * exp_result: Expected result of the comparison, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty dicts
    (
        "Empty dicts with >",
        dict(
            obj1=DictView({}),
            obj2=DictView({}),
            op='>',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Empty dicts with >=",
        dict(
            obj1=DictView({}),
            obj2=DictView({}),
            op='>=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Empty dicts with <",
        dict(
            obj1=DictView({}),
            obj2=DictView({}),
            op='<',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Empty dicts with <=",
        dict(
            obj1=DictView({}),
            obj2=DictView({}),
            op='<=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),

    # Equal dicts
    (
        "Equal dicts with >",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='>',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Equal dicts with >=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='>=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Equal dicts with <",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='<',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Equal dicts with <=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='<=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),

    # Dicts that compare less (obj1 < obj2)
    (
        "Less-comparing dicts with >",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='>',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Less-comparing dicts with >=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='>=',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Less-comparing dicts with <",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='<',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Less-comparing dicts with <=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            op='<=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),

    # Dicts that compare greater (obj1 > obj2)
    (
        "Greater-comparing dicts with >",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish')])),
            op='>',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Greater-comparing dicts with >=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish')])),
            op='>=',
            exp_result=True,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Greater-comparing dicts with <",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish')])),
            op='<',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),
    (
        "Greater-comparing dicts with <=",
        dict(
            obj1=DictView(OrderedDict([('Budgie', 'Fish'), ('Dog', 'Cat')])),
            obj2=DictView(OrderedDict([('Budgie', 'Fish')])),
            op='<=',
            exp_result=False,
        ),
        None if DICT_SUPPORTS_COMPARISON else TypeError, None, True
    ),

    # Note: More subtle cases of less- or greater-comparing dicts are not
    # tested because the ordering comparison for DictView is deprecated.
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_ORDERING)
@simplified_test_function
def test_DictView_ordering(testcase, obj1, obj2, op, exp_result):
    """
    Test function for DictView.__le__(), __lt__(), __ge__(), __gt__() / ord.
    """

    comp_str = 'obj1 %s obj2' % op

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    result = eval(comp_str)  # pylint: disable=eval-used

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_DICTVIEW_PICKLE = [

    # Testcases for pickling and unpickling DictView objects

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * dictview: DictView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "DictView of empty dict",
        dict(
            dictview=DictView({}),
        ),
        None, None, True
    ),
    (
        "DictView of dict with one item",
        dict(
            dictview=DictView({'Dog': 'Cat'}),
        ),
        None, None, True
    ),
    (
        "DictView of DerivedDict with one item",
        dict(
            dictview=DictView(DerivedDict({'Dog': 'Cat'})),
        ),
        None, None, True
    ),
    (
        "DerivedDictView of dict with one item",
        dict(
            dictview=DerivedDictView(dict({'Dog': 'Cat'})),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_PICKLE)
@simplified_test_function
def test_DictView_pickle(testcase, dictview):
    """
    Test function for pickling and unpickling DictView objects
    """

    # Pickle the object
    pkl = pickle.dumps(dictview)

    # Unpickle the object
    dictview2 = pickle.loads(pkl)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert dictview2 == dictview


TESTCASES_DICTVIEW_HASH = [

    # Testcases for DictView.__hash__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * dict_obj: Underlying dictionary object.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dict",
        dict(
            dict_obj={},
        ),
        TypeError, None, True
    ),
    (
        "Empty OrderedDict",
        dict(
            dict_obj=OrderedDict(),
        ),
        TypeError, None, True
    ),
    (
        "Empty HashableDict",
        dict(
            dict_obj=HashableDict(),
        ),
        None, None, True
    ),

    (
        "Dict with one item",
        dict(
            dict_obj=dict([('a', 1)]),
        ),
        TypeError, None, True
    ),
    (
        "OrderedDict with one item",
        dict(
            dict_obj=OrderedDict([('a', 1)]),
        ),
        TypeError, None, True
    ),
    (
        "HashableDict with one item",
        dict(
            dict_obj=HashableDict([('a', 1)]),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_HASH)
@simplified_test_function
def test_DictView_hash(testcase, dict_obj):
    """
    Test function for DictView.__hash__() / hash()
    """

    view = DictView(dict_obj)

    # The code to be tested
    view_hash = hash(view)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # If it worked for the view, it must work for the underlying collection
    dict_hash = hash(dict_obj)

    # Verify the hash value of the underlying collection is used for the view
    assert view_hash == dict_hash


TESTCASES_DICTVIEW_OR = [

    # Testcases for DictView.__or__/__ror__() / self | or

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: DictView object #1 to be used.
    #   * obj2: DictView object #2 to be used.
    #   * exp_result: Expected result of the operation, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "DictView of empty NorDict and DictView of empty NorDict",
        dict(
            obj1=DictView(NorDict()),
            obj2=DictView(NorDict()),
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "DictView of empty OrDict and DictView of empty NorDict",
        dict(
            obj1=DictView(OrDict()),
            obj2=DictView(NorDict()),
            exp_result=DictView(OrDict()),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "DictView of empty NorDict and DictView of empty OrDict",
        dict(
            obj1=DictView(NorDict()),
            obj2=DictView(OrDict()),
            exp_result=DictView(NorDict()),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "Empty NorDict and DictView of empty OrDict",
        dict(
            obj1=NorDict(),
            obj2=DictView(OrDict()),
            exp_result=NorDict(),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),

    (
        "OrDict with two items and NorDict with equal two items",
        dict(
            obj1=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            obj2=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            exp_result=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "NorDict with two items and OrDict with equal two items",
        dict(
            obj1=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            obj2=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            exp_result=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),

    (
        "Empty OrDict and NorDict with two items",
        dict(
            obj1=DictView(OrDict()),
            obj2=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            exp_result=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "Empty NorDict and OrDict with two items",
        dict(
            obj1=DictView(NorDict()),
            obj2=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            exp_result=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),

    (
        "OrDict with two items and empty NorDict",
        dict(
            obj1=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            obj2=DictView(NorDict()),
            exp_result=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "NorDict with two items and empty OrDict",
        dict(
            obj1=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
            obj2=DictView(OrDict()),
            exp_result=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),

    (
        "OrDict with one item and NorDict with one item with different key",
        dict(
            obj1=DictView(OrDict({'Budgie': 'Fish'})),
            obj2=DictView(NorDict({'Dog': 'Cat'})),
            exp_result=DictView(OrDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "NorDict with one item and OrDict with one item with different key",
        dict(
            obj1=DictView(NorDict({'Budgie': 'Fish'})),
            obj2=DictView(OrDict({'Dog': 'Cat'})),
            exp_result=DictView(NorDict({'Budgie': 'Fish', 'Dog': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),

    (
        "OrDict with one item and NorDict with one item with same key, "
        "different value",
        dict(
            obj1=DictView(OrDict({'Budgie': 'Fish'})),
            obj2=DictView(NorDict({'Budgie': 'Cat'})),
            exp_result=DictView(NorDict({'Budgie': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
    (
        "NorDict with one item and OrDict with one item with same key, "
        "different value",
        dict(
            obj1=DictView(NorDict({'Budgie': 'Fish'})),
            obj2=DictView(OrDict({'Budgie': 'Cat'})),
            exp_result=DictView(NorDict({'Budgie': 'Cat'})),
        ),
        None if DICT_SUPPORTS_OR else TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DICTVIEW_OR)
@simplified_test_function
def test_DictView_or(testcase, obj1, obj2, exp_result):
    """
    Test function for DictView.__or__/__ror__() / self | or
    """

    # The code to be tested
    result = obj1 | obj2

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result
