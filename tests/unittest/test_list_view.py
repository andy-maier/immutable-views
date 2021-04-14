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
Test the ListView class.
"""

from __future__ import absolute_import

import sys
import re
import pickle
try:
    from collections.abc import Sequence, MutableSequence
except ImportError:
    # Python 2
    from collections import Sequence, MutableSequence
import pytest
from nocaselist import NocaseList

from ..utils.simplified_test_function import simplified_test_function

# pylint: disable=wrong-import-position, wrong-import-order, invalid-name
from ..utils.import_installed import import_installed
immutable_views = import_installed('immutable_views')
from immutable_views import ListView  # noqa: E402
# pylint: enable=wrong-import-position, wrong-import-order, invalid-name

# Indicates that the list to be tested has a copy() method
LIST_HAS_COPY = sys.version_info[0] == 3

# Indicates that the list to be tested has a clear() method
LIST_HAS_CLEAR = sys.version_info[0] == 3

# Flag indicating that standard dict is guaranteed to preserve order
DICT_PRESERVES_ORDER = sys.version_info[0:2] >= (3, 7)


class DerivedList(list):
    """List derived from list with additional attribute"""

    def __init__(self, *args, **kwargs):
        super(DerivedList, self).__init__(*args, **kwargs)
        self._dummy = 'dummy'

    def __eq__(self, other):
        super_equal = super(DerivedList, self).__eq__(other)
        if isinstance(other, DerivedList):
            return super_equal and self._dummy == other._dummy
        return super_equal


class DerivedListView(ListView):
    """List view derived from ListView with additional attribute"""

    def __init__(self, *args, **kwargs):
        super(DerivedListView, self).__init__(*args, **kwargs)
        self._dummy = 'dummy'

    def __eq__(self, other):
        super_equal = super(DerivedListView, self).__eq__(other)
        if isinstance(other, DerivedListView):
            return super_equal and self._dummy == other._dummy
        return super_equal


def assert_equal(list1, list2, verify_order=True):
    """
    Assert that list1 is equal to list2.

    list1: Must be an iterable object, including ListView.
    list2: Must be an iterable object, including ListView.
    """

    list1_lst = list(list1)  # Uses ListView.__iter__()
    list2_lst = list(list2)  # Uses ListView.__iter__()

    if verify_order:
        assert list1_lst == list2_lst
    else:
        assert sorted(list1_lst) == sorted(list2_lst)


def get_a_list_arg(a_list):
    "Get the a_list argument"
    return a_list


TESTCASES_LISTVIEW_INIT = [

    # Testcases for ListView.__init__() / lv=ListView()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to ListView().
    #   * init_kwargs: Dict of keyword arguments to ListView().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty underlying sequences
    (
        "From empty list as positional arg",
        dict(
            init_args=([],),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From empty tuple as positional arg",
        dict(
            init_args=(tuple(),),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From empty unicode string as positional arg",
        dict(
            init_args=(u'',),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From empty byte string as positional arg",
        dict(
            init_args=(b'',),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From ListView of empty list as positional arg",
        dict(
            init_args=(ListView([]),),
            init_kwargs=dict(),
        ),
        None, None, True
    ),

    # Non-empty underlying sequence
    (
        "From non-empty list as positional arg",
        dict(
            init_args=(['Dog', 'Cat'],),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From non-empty tuple as positional arg",
        dict(
            init_args=(('Dog', 'Cat'),),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From string as positional arg",
        dict(
            init_args=('Dog',),
            init_kwargs=dict(),
        ),
        None, None, True
    ),

    # Errors with input parameters that would work fine with a list/tuple
    (
        "No args (missing parameter)",
        dict(
            init_args=(),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty dict as positional arg (must be Sequence)",
        dict(
            init_args=({},),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From dict as positional arg (must be Sequence)",
        dict(
            init_args=({'Dog': 'Kitten', 'Cat': 'Budgie'},),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),

    # Other error cases
    (
        "From 'iterable' keyword arg (no kwargs)",
        dict(
            init_args=(),
            init_kwargs=dict(iterable=[1, 2]),
        ),
        TypeError, None, True
    ),
    (
        "From None as positional arg (is not iterable)",
        dict(
            init_args=(None,),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From integer as positional arg",
        dict(
            init_args=(42,),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From two positional args",
        dict(
            init_args=([], []),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_INIT)
@simplified_test_function
def test_ListView_init(testcase, init_args, init_kwargs):
    """
    Test function for ListView.__init__() / lv=ListView()
    """

    # The code to be tested
    listview = ListView(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    a_list_arg = get_a_list_arg(*init_args, **init_kwargs)
    listview_list = listview.list

    # Verify that ListView inherits from Sequence
    assert isinstance(listview, Sequence)

    # Verify the underlying list object's identity
    if isinstance(a_list_arg, ListView):
        assert listview_list is a_list_arg.list
    else:
        assert listview_list is a_list_arg


TESTCASES_LISTVIEW_REPR = [

    # Testcases for ListView.__repr__() / repr(lv)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "ListView of empty list",
        dict(
            listview=ListView([]),
        ),
        None, None, True
    ),
    (
        "ListView of list with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items",
        dict(
            listview=ListView(('Dog', 'Cat')),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_REPR)
@simplified_test_function
def test_ListView_repr(testcase, listview):
    """
    Test function for ListView.__repr__() / repr(lv)
    """

    # The code to be tested
    result = repr(listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert re.match(r'^ListView\(.*\)$', result)

    # Note: This only tests for existence of each item, not for excess items
    # or representing the correct order.
    for item in listview:
        exp_item_result = repr(item)
        assert exp_item_result in result


TESTCASES_LISTVIEW_GETITEM = [

    # Testcases for ListView.__getitem__() / val = lv[idx]

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * index: Index to be used for the test.
    #   * exp_value: Expected value for the index.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty ListView
    (
        "ListView of empty list, with None as index (invalid type)",
        dict(
            listview=ListView([]),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of empty list, with string as index (invalid type)",
        dict(
            listview=ListView([]),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of empty list, with non-existing index 0 (out of range)",
        dict(
            listview=ListView([]),
            index=0,
            exp_value=None,
        ),
        IndexError, None, True
    ),
    (
        "ListView of empty tuple, with None as index (invalid type)",
        dict(
            listview=ListView(tuple()),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of empty tuple, with string as index (invalid type)",
        dict(
            listview=ListView(tuple()),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of empty tuple, with non-existing index 0 (out of range)",
        dict(
            listview=ListView(tuple()),
            index=0,
            exp_value=None,
        ),
        IndexError, None, True
    ),

    # Non-empty ListView
    (
        "ListView of list with two items, with None as index (invalid type)",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of list with two items, with string as index (invalid type)",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of list with two items, with non-existing index 2 "
        "(out of range)",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index=2,
            exp_value=None,
        ),
        IndexError, None, True
    ),
    (
        "ListView of list with two items, with index 0",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index=0,
            exp_value='Dog',
        ),
        None, None, True
    ),
    (
        "ListView of list with two items, with index 1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index=1,
            exp_value='Cat',
        ),
        None, None, True
    ),
    (
        "ListView of list with two items, with index -1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            index=-1,
            exp_value='Cat',
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items, with None as index (invalid type)",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of tuple with two items, with string as index (invalid type)",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "ListView of tuple with two items, with non-existing index 2 "
        "(out of range)",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index=2,
            exp_value=None,
        ),
        IndexError, None, True
    ),
    (
        "ListView of tuple with two items, with index 0",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index=0,
            exp_value='Dog',
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items, with index 1",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index=1,
            exp_value='Cat',
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items, with index -1",
        dict(
            listview=ListView(('Dog', 'Cat')),
            index=-1,
            exp_value='Cat',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_GETITEM)
@simplified_test_function
def test_ListView_getitem(testcase, listview, index, exp_value):
    """
    Test function for ListView.__getitem__() / val = lv[idx]
    """

    # The code to be tested
    act_value = listview[index]

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_value == exp_value, "Unexpected value at index {}".format(index)


def test_ListView_setitem():
    """
    Test function for the non-existing ListView.__setitem__() / lv[idx]=value
    """
    listview = ListView(['a'])

    with pytest.raises(TypeError) as exc_info:
        # The code to be tested
        listview[0] = 'b'  # pylint: disable=unsupported-assignment-operation

    exc_msg = str(exc_info.value)
    assert re.search(r"does not support item assignment", exc_msg)


def test_ListView_delitem():
    """
    Test function for the non-existing ListView.__delitem__() / del lv[idx]
    """
    listview = ListView(['a'])

    with pytest.raises(TypeError) as exc_info:
        # The code to be tested
        del listview[0]  # pylint: disable=unsupported-delete-operation

    exc_msg = str(exc_info.value)
    assert re.search(r"doesn't support item deletion", exc_msg)


TESTCASES_LISTVIEW_ITER = [

    # Testcases for ListView.__iter__() / for item in lv

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * exp_items: List with expected items in expected order.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "ListView of empty list",
        dict(
            listview=ListView([]),
            exp_items=[],
        ),
        None, None, True
    ),
    (
        "ListView of empty tuple",
        dict(
            listview=ListView(tuple()),
            exp_items=[],
        ),
        None, None, True
    ),
    (
        "ListView of empty string",
        dict(
            listview=ListView(''),
            exp_items=[],
        ),
        None, None, True
    ),
    (
        "ListView of list with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
            exp_items=['Dog', 'Cat'],
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items",
        dict(
            listview=ListView(('Dog', 'Cat')),
            exp_items=['Dog', 'Cat'],
        ),
        None, None, True
    ),
    (
        "ListView of non-empty string with two characters",
        dict(
            listview=ListView(('ab')),
            exp_items=['a', 'b'],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_ITER)
@simplified_test_function
def test_ListView_iter(testcase, listview, exp_items):
    """
    Test function for ListView.__iter__() / for item in lv
    """

    # The code to be tested
    act_items = []
    for item in listview:
        act_items.append(item)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_items == exp_items


TESTCASES_LISTVIEW_CONTAINS = [

    # Testcases for ListView.__contains__() / value in lv

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * value: Value to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty ListView
    (
        "Empty list, with None as value",
        dict(
            listview=ListView([]),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with integer value 0",
        dict(
            listview=ListView([]),
            value=0,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-existing empty value (not found)",
        dict(
            listview=ListView([]),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-existing non-empty value (not found)",
        dict(
            listview=ListView([]),
            value='Dog',
            exp_result=False,
        ),
        None, None, True
    ),

    # Non-empty ListView
    (
        "List with two items, with None as value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with integer value 0",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value=0,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing empty value (not found)",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing non-empty value (not found)",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='invalid',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='Dog',
            exp_result=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_CONTAINS)
@simplified_test_function
def test_ListView_contains(testcase, listview, value, exp_result):
    """
    Test function for ListView.__contains__() / value in lv
    """

    # The code to be tested
    act_result = value in listview

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result, \
        "Unexpected result for value {!r}".format(value)


TESTCASES_LISTVIEW_SIZEOF = [

    # Testcases for ListView.__sizeof__() / len(lv)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            listview=ListView([]),
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
            exp_result=2,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_SIZEOF)
@simplified_test_function
def test_ListView_sizeof(testcase, listview, exp_result):
    """
    Test function for ListView.__sizeof__() / len(lv)
    """

    # The code to be tested
    result = len(listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_LISTVIEW_ADD = [

    # Testcases for ListView.__add__() / lv + val

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView (LHO) object to be used for the test.
    #   * other: Other iterable (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Add a ListView of an empty list and a string "
        "(list can only concatenate list)",
        dict(
            listview=ListView([]),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Add a ListView of an empty list and a string "
        "(list can only concatenate list)",
        dict(
            listview=ListView([]),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Add a ListView of an empty list and a tuple "
        "(list can only concatenate list)",
        dict(
            listview=ListView([]),
            other=('Dog',),
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Add a ListView of an empty tuple and a tuple",
        dict(
            listview=ListView(tuple()),
            other=('Dog',),
            exp_result=ListView(('Dog',)),
        ),
        None, None, True
    ),
    (
        "Add an empty ListView and a list with one string item",
        dict(
            listview=ListView([]),
            other=['Dog'],
            exp_result=ListView(['Dog']),
        ),
        None, None, True
    ),
    (
        "Add an empty ListView and a ListView with one string item",
        dict(
            listview=ListView([]),
            other=ListView(['Dog']),
            exp_result=ListView(['Dog']),
        ),
        None, None, True
    ),
    (
        "Add an empty ListView and a list with one integer item",
        dict(
            listview=ListView([]),
            other=[42],
            exp_result=ListView([42]),
        ),
        None, None, True
    ),
    (
        "Add a ListView with two items and a list with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
            other=['Budgie', 'Fish'],
            exp_result=ListView(['Dog', 'Cat', 'Budgie', 'Fish']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_ADD)
@simplified_test_function
def test_ListView_add(testcase, listview, other, exp_result):
    """
    Test function for ListView.__add__() / lv + val
    """

    org_listview = ListView(listview)

    # The code to be tested
    result = listview + other

    # Verify the input ListView object has not changed
    assert_equal(listview, org_listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_LISTVIEW_IADD = [

    # Testcases for ListView.__iadd__() / lv += val

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView (LHO) object to be used for the test.
    #   * other: Other iterable (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Extend a ListView of an empty list by a string "
        "(list can only concatenate list)",
        dict(
            listview=ListView([]),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Extend a ListView of an empty list by an integer (no iterable)",
        dict(
            listview=ListView([]),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Extend a ListView of an empty list by a non-empty tuple "
        "(list can only concatenate list)",
        dict(
            listview=ListView([]),
            other=('Dog',),
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Extend a ListView of an empty tuple by a non-empty tuple",
        dict(
            listview=ListView(tuple()),
            other=('Dog',),
            exp_result=ListView(('Dog',)),
        ),
        None, None, True
    ),
    (
        "Extend a ListView of an empty list by a non-empty list",
        dict(
            listview=ListView([]),
            other=['Dog'],
            exp_result=ListView(['Dog']),
        ),
        None, None, True
    ),
    (
        "Extend a ListView of an empty list by a ListView of a non-empty list",
        dict(
            listview=ListView([]),
            other=ListView(['Dog']),
            exp_result=ListView(['Dog']),
        ),
        None, None, True
    ),
    (
        "Extend a ListView of a non-empty list by a non-empty list",
        dict(
            listview=ListView(['Dog', 'Cat']),
            other=['Budgie', 'Fish'],
            exp_result=ListView(['Dog', 'Cat', 'Budgie', 'Fish']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_IADD)
@simplified_test_function
def test_ListView_iadd(testcase, listview, other, exp_result):
    """
    Test function for ListView.__iadd__() / lv += val
    """

    # Don't change the testcase data, but a copy
    listview_copy = ListView(listview)
    listview_copy_id = id(listview_copy)

    # The code to be tested
    listview_copy += other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `+=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __iadd__() results in Python calling
    # __add__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__iadd__.
    # For Listview, the `+=` operator results in a new ListView object on a new
    # underlying list object.
    assert id(listview_copy) != listview_copy_id

    assert_equal(listview_copy, exp_result)


TESTCASES_LISTVIEW_MUL = [

    # Testcases for ListView.__mul__() / lv * num
    # Testcases for ListView.__rmul__() / num * lv
    # Testcases for ListView.__imul__() / lv *= num

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * number: Number parameter for the test function.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list times -1",
        dict(
            listview=ListView([]),
            number=-1,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "Empty list times 0",
        dict(
            listview=ListView([]),
            number=0,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "Empty list times 1",
        dict(
            listview=ListView([]),
            number=1,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "Empty list times 2",
        dict(
            listview=ListView([]),
            number=2,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "Empty list times -0.5 (must be integer)",
        dict(
            listview=ListView([]),
            number=-0.5,
            exp_result=ListView([]),
        ),
        TypeError, None, True
    ),
    (
        "Empty list times +0.5 (must be integer)",
        dict(
            listview=ListView([]),
            number=+0.5,
            exp_result=ListView([]),
        ),
        TypeError, None, True
    ),
    (
        "List with two items times -1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            number=-1,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "List with two items times 0",
        dict(
            listview=ListView(['Dog', 'Cat']),
            number=0,
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "List with two items times 1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            number=1,
            exp_result=ListView(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items times 2",
        dict(
            listview=ListView(['Dog', 'Cat']),
            number=2,
            exp_result=ListView(['Dog', 'Cat', 'Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_MUL)
@simplified_test_function
def test_ListView_mul(testcase, listview, number, exp_result):
    """
    Test function for ListView.__mul__() / lv * num
    """

    org_listview = ListView(listview)

    # The code to be tested
    result = listview * number

    # Verify the input ListView object has not changed
    assert_equal(listview, org_listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_MUL)
@simplified_test_function
def test_ListView_rmul(testcase, listview, number, exp_result):
    """
    Test function for ListView.__rmul__() / num * lv
    """

    org_listview = ListView(listview)

    # The code to be tested
    result = number * listview

    # Verify the input ListView object has not changed
    assert_equal(listview, org_listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_MUL)
@simplified_test_function
def test_ListView_imul(testcase, listview, number, exp_result):
    """
    Test function for ListView.__imul__() / lv *= num
    """

    # Don't change the testcase data, but a copy
    listview_copy = ListView(listview)
    listview_copy_id = id(listview_copy)

    # The code to be tested
    listview_copy *= number

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `*=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __imul__() results in Python calling
    # __mul__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__imul__.
    # For Listview, the `*=` operator results in a new ListView object on a new
    # underlying list object.
    assert id(listview_copy) != listview_copy_id

    assert_equal(listview_copy, exp_result)


TESTCASES_LISTVIEW_REVERSED = [

    # Testcases for ListView.__reversed__() / reversed(lv)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            listview=ListView([]),
            exp_result=ListView([]),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
            exp_result=ListView(['Cat', 'Dog']),
        ),
        None, None, True
    ),
    (
        "List with three items",
        dict(
            listview=ListView(['Dog', 'Cat', 'Kitten']),
            exp_result=ListView(['Kitten', 'Cat', 'Dog']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_REVERSED)
@simplified_test_function
def test_ListView_reversed(testcase, listview, exp_result):
    """
    Test function for ListView.__reversed__() / reversed(lv)
    """

    org_listview = ListView(listview)

    # The code to be tested
    result = reversed(listview)

    # Verify the input ListView object has not changed
    assert_equal(listview, org_listview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


def test_ListView_reverse():
    """
    Test function for the non-existing ListView.reverse()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.reverse()  # pylint: disable=no-member


TESTCASES_LISTVIEW_COMPARE = [

    # Testcases for ListView.__eq__(), __ne__()
    # Testcases for ListView.__gt__(), __le__()
    # Testcases for ListView.__lt__(), __ge__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: ListView object #1 to use.
    #   * obj2: ListView object #2 to use.
    #   * exp_eq: Expected result of __eq__() and !__ne__()
    #   * exp_gt: Expected result of __gt__() and !__le__()
    #   * exp_lt: Expected result of __lt__() and !__ge__()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Compare ListView of empty list with ListView of empty list",
        dict(
            obj1=ListView([]),
            obj2=ListView([]),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView of empty tuple with ListView of empty tuple",
        dict(
            obj1=ListView(tuple()),
            obj2=ListView(tuple()),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView of empty list with empty list",
        dict(
            obj1=ListView([]),
            obj2=[],
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare empty list with ListView of empty list",
        dict(
            obj1=[],
            obj2=ListView([]),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView of empty tuple with empty tuple",
        dict(
            obj1=ListView(tuple()),
            obj2=tuple(),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare empty tuple with ListView of empty tuple",
        dict(
            obj1=tuple(),
            obj2=ListView(tuple()),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),

    (
        "Compare ListView of list with one item with equal ListView",
        dict(
            obj1=ListView(['Cat']),
            obj2=ListView(['Cat']),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView of list with one item with equal list",
        dict(
            obj1=ListView(['Cat']),
            obj2=['Cat'],
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare list with one item with equal ListView of list",
        dict(
            obj1=['Cat'],
            obj2=ListView(['Cat']),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView of tuple with one item with equal tuple",
        dict(
            obj1=ListView(('Cat',)),
            obj2=('Cat',),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare tuple with one item with ListView of equal tuple",
        dict(
            obj1=('Cat',),
            obj2=ListView(('Cat',)),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),

    (
        "Compare ListView with one item with empty ListView (is greater than)",
        dict(
            obj1=ListView(['Cat']),
            obj2=ListView([]),
            exp_eq=False,
            exp_gt=True,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare empty ListView with ListView with one item (is less than)",
        dict(
            obj1=ListView([]),
            obj2=ListView(['Cat']),
            exp_eq=False,
            exp_gt=False,
            exp_lt=True,
        ),
        None, None, True
    ),
    (
        "Compare ListView with one item with ListView with one lesser item "
        "(is greater than)",
        dict(
            obj1=ListView(['Dog']),
            obj2=ListView(['Cat']),
            exp_eq=False,
            exp_gt=True,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Compare ListView with one item with ListView with one greater item "
        "(is less than)",
        dict(
            obj1=ListView(['Cat']),
            obj2=ListView(['Dog']),
            exp_eq=False,
            exp_gt=False,
            exp_lt=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_eq(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__eq__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    eq1 = (obj1 == obj2)
    eq2 = (obj2 == obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert eq1 == exp_eq
    assert eq2 == exp_eq


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_ne(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__ne__()
    """

    exp_ne = not exp_eq

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    ne1 = (obj1 != obj2)
    ne2 = (obj2 != obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert ne1 == exp_ne
    assert ne2 == exp_ne


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_gt(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__gt__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    gt = (obj1 > obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert gt == exp_gt


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_lt(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__lt__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    lt = (obj1 < obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert lt == exp_lt


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_ge(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__ge__()
    """

    exp_ge = not exp_lt

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    ge = (obj1 >= obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert ge == exp_ge


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COMPARE)
@simplified_test_function
def test_ListView_le(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for ListView.__le__()
    """

    exp_le = not exp_gt

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    le = (obj1 <= obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert le == exp_le


TESTCASES_LISTVIEW_COUNT = [

    # Testcases for ListView.count()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * value: Value parameter for the test function.
    #   * exp_result: Expected result of the test function.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty ListView
    (
        "Empty list, with integer value",
        dict(
            listview=ListView([]),
            value=1234,
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-empty string value",
        dict(
            listview=ListView([]),
            value='Cat',
            exp_result=0,
        ),
        None, None, True
    ),

    # Non-empty ListView
    (
        "List with two items, with integer value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value=1234,
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-matching empty string value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='',
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-matching string value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='Kitten',
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with value matching one list item",
        dict(
            listview=ListView(['Dog', 'Cat']),
            value='Cat',
            exp_result=1,
        ),
        None, None, True
    ),
    (
        "List with four items, with value matching three list items",
        dict(
            listview=ListView(['Cat', 'Dog', 'Cat', 'Cat']),
            value='Cat',
            exp_result=3,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COUNT)
@simplified_test_function
def test_ListView_count(testcase, listview, value, exp_result):
    """
    Test function for ListView.count()
    """

    # The code to be tested
    result = listview.count(value)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_LISTVIEW_COPY = [

    # Testcases for ListView.copy()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "ListView of empty list",
        dict(
            listview=ListView([]),
        ),
        None, None, True
    ),
    (
        "ListView of list with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "ListView of empty tuple",
        dict(
            listview=ListView(tuple()),
        ),
        None, None, True
    ),
    (
        "ListView of tuple with two items",
        dict(
            listview=ListView(('Dog', 'Cat')),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_COPY)
@simplified_test_function
def test_ListView_copy(testcase, listview):
    """
    Test function for ListView.copy()
    """

    listview_list = listview.list

    # The code to be tested
    listview_copy = listview.copy()

    listview_copy_list = listview_copy.list

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the result type
    # pylint: disable=unidiomatic-typecheck
    assert type(listview_copy) is ListView

    # Verify the result is a different object than the ListView
    assert id(listview_copy) != id(listview)

    # Verify the new list is a different object than the underlying list,
    # if mutable
    if isinstance(listview_list, MutableSequence):
        assert id(listview_copy_list) != id(listview_list)

    # Verify the new list has the same type as the underlying list
    # pylint: disable=unidiomatic-typecheck
    assert type(listview_copy_list) == type(listview_list)

    # Verify the new list is equal to the underlying list
    assert listview_copy_list == listview_list


def test_ListView_clear():
    """
    Test function for the non-existing ListView.clear()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.clear()  # pylint: disable=no-member


TESTCASES_LISTVIEW_INDEX = [

    # Testcases for ListView.index()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    #   * args: Positional arguments for the test function.
    #   * exp_result: Expected result of the test function.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty ListView
    (
        "Empty list, with non-existing integer value (not in list)",
        dict(
            listview=ListView([]),
            args=(1234,),
            exp_result=None,
        ),
        ValueError, None, True
    ),
    (
        "Empty list, with non-existing string value (not in list)",
        dict(
            listview=ListView([]),
            args=('Cat',),
            exp_result=None
        ),
        ValueError, None, True
    ),

    # Non-empty ListView
    (
        "List with two items, with non-existing integer value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=(1234,),
            exp_result=None,
        ),
        ValueError, None, True
    ),
    (
        "List with two items, with non-existing empty string value",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=('',),
            exp_result=None,
        ),
        ValueError, None, True
    ),
    (
        "List with two items, with existing string value at index 0",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=('Dog',),
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing string value at index 1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=('Cat',),
            exp_result=1,
        ),
        None, None, True
    ),
    (
        "List with two items, with start at 1 and string value of index 0",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=('Dog', 1),
            exp_result=None,
        ),
        ValueError, None, True
    ),
    (
        "List with two items, with start at 1 and string value of index 1",
        dict(
            listview=ListView(['Dog', 'Cat']),
            args=('Cat', 1),
            exp_result=1,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_INDEX)
@simplified_test_function
def test_ListView_index(testcase, listview, args, exp_result):
    """
    Test function for ListView.index()
    """

    # The code to be tested
    result = listview.index(*args)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


def test_ListView_append():
    """
    Test function for the non-existing ListView.append()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.append('b')  # pylint: disable=no-member


def test_ListView_extend():
    """
    Test function for the non-existing ListView.extend()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.extend(['b'])  # pylint: disable=no-member


def test_ListView_insert():
    """
    Test function for the non-existing ListView.insert()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.insert(0, 'b')  # pylint: disable=no-member


def test_ListView_pop():
    """
    Test function for the non-existing ListView.pop()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.pop()  # pylint: disable=no-member


def test_ListView_remove():
    """
    Test function for the non-existing ListView.remove()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.remove('a')  # pylint: disable=no-member


def test_ListView_sort():
    """
    Test function for the non-existing ListView.sort()
    """
    listview = ListView(['a'])

    with pytest.raises(AttributeError):
        # The code to be tested
        listview.sort()  # pylint: disable=no-member


TESTCASES_LISTVIEW_PICKLE = [

    # Testcases for pickling and unpickling ListView objects

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listview: ListView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "ListView of empty list",
        dict(
            listview=ListView([]),
        ),
        None, None, True
    ),
    (
        "ListView of list with two items",
        dict(
            listview=ListView(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "ListView of DerivedList with two items",
        dict(
            listview=ListView(DerivedList(['Dog', 'Cat'])),
        ),
        None, None, True
    ),
    (
        "DerivedListView of list with two items",
        dict(
            listview=DerivedListView(['Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_PICKLE)
@simplified_test_function
def test_ListView_pickle(testcase, listview):
    """
    Test function for pickling and unpickling ListView objects
    """

    # Pickle the object
    pkl = pickle.dumps(listview)

    # Unpickle the object
    listview2 = pickle.loads(pkl)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(listview2, listview)


TESTCASES_LISTVIEW_HASH = [

    # Testcases for ListView.__hash__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * list_obj: Underlying list object.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            list_obj=[],
        ),
        TypeError, None, True
    ),
    (
        "Empty tuple",
        dict(
            list_obj=tuple(),
        ),
        None, None, True
    ),
    (
        "Empty NocaseList",
        dict(
            list_obj=NocaseList(),
        ),
        TypeError, None, True
    ),

    (
        "List with one item",
        dict(
            list_obj=['a'],
        ),
        TypeError, None, True
    ),
    (
        "Tuple with one item",
        dict(
            list_obj=('a',),
        ),
        None, None, True
    ),
    (
        "NocaseList with one item",
        dict(
            list_obj=NocaseList(['a']),
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTVIEW_HASH)
@simplified_test_function
def test_ListView_hash(testcase, list_obj):
    """
    Test function for ListView.__hash__() / hash()
    """

    view = ListView(list_obj)

    # The code to be tested
    view_hash = hash(view)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # If it worked for the view, it must work for the underlying collection
    list_hash = hash(list_obj)

    # Verify the hash value of the underlying collection is used for the view
    assert view_hash == list_hash
