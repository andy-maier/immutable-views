"""
Test the SetView class.
"""

from __future__ import absolute_import

import sys
import re
import pickle
try:
    from collections.abc import Set, MutableSet
except ImportError:
    # Python 2
    from collections import Set, MutableSet
import pytest

from ..utils.simplified_test_function import simplified_test_function

# pylint: disable=wrong-import-position, wrong-import-order, invalid-name
from ..utils.import_installed import import_installed
immutable_views = import_installed('immutable_views')
from immutable_views import SetView  # noqa: E402
# pylint: enable=wrong-import-position, wrong-import-order, invalid-name

# Indicates that the list to be tested has a copy() method
LIST_HAS_COPY = sys.version_info[0] == 3

# Indicates that the list to be tested has a clear() method
LIST_HAS_CLEAR = sys.version_info[0] == 3

# Flag indicating that standard dict is guaranteed to preserve order
DICT_PRESERVES_ORDER = sys.version_info[0:2] >= (3, 7)


def assert_equal(set1, set2):
    """
    Assert that set1 is equal to set2.

    set1: Must be an iterable object, including SetView.
    set2: Must be an iterable object, including SetView.
    """

    set1_lst = list(set1)  # Uses SetView.__iter__()
    set2_lst = list(set2)  # Uses SetView.__iter__()

    assert sorted(set1_lst) == sorted(set2_lst)


def get_a_set_arg(a_set):
    "Get the a_set argument"
    return a_set


TESTCASES_SETVIEW_INIT = [

    # Testcases for SetView.__init__() / sv=SetView()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to SetView().
    #   * init_kwargs: Dict of keyword arguments to SetView().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty original sequences
    (
        "From empty set as positional arg",
        dict(
            init_args=(set(),),
            init_kwargs=dict(),
        ),
        None, None, True
    ),
    (
        "From empty SetView as positional arg",
        dict(
            init_args=(SetView(set()),),
            init_kwargs=dict(),
        ),
        None, None, True
    ),

    # Non-empty original sequence
    (
        "From set with one item as positional arg",
        dict(
            init_args=({'Dog', 'Cat'},),
            init_kwargs=dict(),
        ),
        None, None, True
    ),

    # Errors with input parameters that would work fine with a set
    (
        "No args (missing parameter)",
        dict(
            init_args=(),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty dict as positional arg (must be Set)",
        dict(
            init_args=({},),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty list as positional arg",
        dict(
            init_args=([],),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty tuple as positional arg",
        dict(
            init_args=(tuple(),),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty unicode string as positional arg",
        dict(
            init_args=(u'',),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From empty byte string as positional arg",
        dict(
            init_args=(b'',),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),


    # Other error cases
    (
        "From None as positional arg (must be Set)",
        dict(
            init_args=(None,),
            init_kwargs=dict(),
        ),
        TypeError, None, True
    ),
    (
        "From integer as positional arg (must be Set)",
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
    TESTCASES_SETVIEW_INIT)
@simplified_test_function
def test_SetView_init(testcase, init_args, init_kwargs):
    """
    Test function for SetView.__init__() / sv=SetView()
    """

    # The code to be tested
    setview = SetView(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    a_set_arg = get_a_set_arg(*init_args, **init_kwargs)
    setview_set = setview._set  # pylint: disable=protected-access

    # Verify that SetView inherits from Set
    assert isinstance(setview, Set)

    # Verify the original set object's identity
    if isinstance(a_set_arg, SetView):
        assert setview_set is a_set_arg._set  # pylint: disable=protected-access
    else:
        assert setview_set is a_set_arg


TESTCASES_SETVIEW_REPR = [

    # Testcases for SetView.__repr__() / repr(sv)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "empty SetView",
        dict(
            setview=SetView(set()),
        ),
        None, None, True
    ),
    (
        "SetView of set with two items",
        dict(
            setview=SetView({'Dog', 'Cat'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_REPR)
@simplified_test_function
def test_SetView_repr(testcase, setview):
    """
    Test function for SetView.__repr__() / repr(sv)
    """

    # The code to be tested
    result = repr(setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert re.match(r'^SetView\(.*\)$', result)

    # Note: This only tests for existence of each item, not for excess items
    # or representing the correct order.
    for item in setview:
        exp_item_result = repr(item)
        assert exp_item_result in result


TESTCASES_SETVIEW_ITER = [

    # Testcases for SetView.__iter__() / for item in sv

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * exp_items: Set with expected items.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "empty SetView",
        dict(
            setview=SetView(set()),
            exp_items=set(),
        ),
        None, None, True
    ),
    (
        "SetView of set with two items",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            exp_items={'Dog', 'Cat'},
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_ITER)
@simplified_test_function
def test_SetView_iter(testcase, setview, exp_items):
    """
    Test function for SetView.__iter__() / for item in sv
    """

    # The code to be tested
    act_items = set()
    for item in setview:
        act_items.add(item)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_items == exp_items


TESTCASES_SETVIEW_CONTAINS = [

    # Testcases for SetView.__contains__() / value in sv

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * value: Value to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty set
    (
        "empty SetView, with None as value",
        dict(
            setview=SetView(set()),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "empty SetView, with integer value 0",
        dict(
            setview=SetView(set()),
            value=0,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "empty SetView, with non-existing empty value (not found)",
        dict(
            setview=SetView(set()),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "empty SetView, with non-existing non-empty value (not found)",
        dict(
            setview=SetView(set()),
            value='Dog',
            exp_result=False,
        ),
        None, None, True
    ),

    # Non-empty set
    (
        "SetView of set with two items, with None as value",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "SetView of set with two items, with integer value 0",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            value=0,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "SetView of set with two items, with non-existing empty value "
        "(not found)",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "SetView of set with two items, with non-existing non-empty value "
        "(not found)",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            value='invalid',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "SetView of set with two items, with existing value",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            value='Dog',
            exp_result=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_CONTAINS)
@simplified_test_function
def test_SetView_contains(testcase, setview, value, exp_result):
    """
    Test function for SetView.__contains__() / value in sv
    """

    # The code to be tested
    act_result = value in setview

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result, \
        "Unexpected result for value {!r}".format(value)


TESTCASES_SETVIEW_LEN = [

    # Testcases for SetView.__len__() / len(sv)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            setview=SetView(set()),
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            exp_result=2,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_LEN)
@simplified_test_function
def test_SetView_len(testcase, setview, exp_result):
    """
    Test function for SetView.__len__() / len(sv)
    """

    # The code to be tested
    result = len(setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_SETVIEW_AND = [

    # Testcases for SetView: self & other (= __and__() / __rand__())
    # Testcases for SetView: self &= other (= __iand__() / __and__() + assign)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView (LHO) object to be used for the test.
    #   * other: Other object (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "and: Empty SetView and an integer (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "and: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            other={'Dog'},
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: Empty set and SetView with one item",
        dict(
            setview=set(),
            other=SetView({'Dog'}),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            other=SetView({'Dog'}),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: Empty SetView and a string (must be set or Set)",
        dict(
            setview=SetView(set()),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "and: Empty SetView and a list (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "and: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            other=set(),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            other=SetView(set()),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            other=SetView(set()),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "and: SetView with one item and a string (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "and: SetView with one item and a list (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "and: SetView with two items and set with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other={'Cat', 'Fish'},
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
    (
        "and: set with two items and SetView with one of them and "
        "one other",
        dict(
            setview={'Dog', 'Cat'},
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
    (
        "and: SetView with two items and SetView with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_AND)
@simplified_test_function
def test_SetView_and(testcase, setview, other, exp_result):
    """
    Test function for SetView: self & other (= __and__() / __rand__())
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview & other

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_AND)
@simplified_test_function
def test_SetView_iand(testcase, setview, other, exp_result):
    """
    Test function for SetView: self &= other (= __iand__() / __and__() + assign)
    """

    # Don't change the testcase data, but a copy
    setview_copy = SetView(setview)
    setview_copy_id = id(setview_copy)

    # The code to be tested
    setview_copy &= other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `+=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __iand__() results in Python calling
    # __and__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__iand__.
    # For SetView, the `&=` operator results in a new SetView object on a new
    # original set object.
    assert id(setview_copy) != setview_copy_id

    assert_equal(setview_copy, exp_result)


TESTCASES_SETVIEW_INTERSECTION = [

    # Testcases for SetView.intersection()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * other: Other object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "intersection: Empty SetView and an integer (must be iterable)",
        dict(
            setview=SetView(set()),
            others=[42],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "intersection: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            others=[{'Dog'}],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: Empty set and SetView with one item",
        dict(
            setview=set(),
            others=[SetView({'Dog'})],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            others=[SetView({'Dog'})],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: Empty SetView and a string",
        dict(
            setview=SetView(set()),
            others=['Dog'],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: Empty SetView and a list",
        dict(
            setview=SetView(set()),
            others=[['Dog']],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),

    (
        "intersection: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            others=[set()],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            others=[SetView(set())],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            others=[SetView(set())],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: SetView with one item and a (different) string",
        dict(
            setview=SetView({'Dog'}),
            others=['Dog'],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "intersection: SetView with one single-char item and same string",
        dict(
            setview=SetView({'D'}),
            others=['D'],
            exp_result=SetView({'D'}),
        ),
        None, None, True
    ),
    (
        "intersection: SetView with one item and a list with same item",
        dict(
            setview=SetView({'Dog'}),
            others=[['Dog']],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),

    (
        "intersection: SetView with two items and set with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[{'Cat', 'Fish'}],
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
    (
        "intersection: set with two items and SetView with one of them and "
        "one other",
        dict(
            setview={'Dog', 'Cat'},
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
    (
        "intersection: SetView with two items and SetView with one of them "
        "and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_INTERSECTION)
@simplified_test_function
def test_SetView_intersection(testcase, setview, others, exp_result):
    """
    Test function for SetView.intersection()
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview.intersection(*others)

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_SETVIEW_OR = [

    # Testcases for SetView: self | other (= __or__() / __ror__())
    # Testcases for SetView: self |= other (= __ior__() / __or__() + assign)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView (LHO) object to be used for the test.
    #   * other: Other object (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "or: Empty SetView and an integer (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "or: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            other={'Dog'},
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: Empty set and SetView with one item",
        dict(
            setview=set(),
            other=SetView({'Dog'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            other=SetView({'Dog'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: Empty SetView and a string (must be set or Set)",
        dict(
            setview=SetView(set()),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "or: Empty SetView and a list (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "or: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            other=set(),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "or: SetView with one item and a string (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "or: SetView with one item and a list (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "or: SetView with two items and set with one of them and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other={'Cat', 'Fish'},
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "or: set with two items and SetView with one of them and one other",
        dict(
            setview={'Dog', 'Cat'},
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "or: SetView with two items and SetView with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_OR)
@simplified_test_function
def test_SetView_or(testcase, setview, other, exp_result):
    """
    Test function for SetView: self | other (= __or__() / __ror__())
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview | other

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_OR)
@simplified_test_function
def test_SetView_ior(testcase, setview, other, exp_result):
    """
    Test function for SetView: self |= other (= __ior__() / __or__() + assign)
    """

    # Don't change the testcase data, but a copy
    setview_copy = SetView(setview)
    setview_copy_id = id(setview_copy)

    # The code to be tested
    setview_copy |= other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `+=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __ior__() results in Python calling
    # __or__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__ior__.
    # For SetView, the `|=` operator results in a new SetView object on a new
    # original set object.
    assert id(setview_copy) != setview_copy_id

    assert_equal(setview_copy, exp_result)


TESTCASES_SETVIEW_UNION = [

    # Testcases for SetView.union()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * other: Other object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "union: Empty SetView and an integer (must be iterable)",
        dict(
            setview=SetView(set()),
            others=[42],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "union: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            others=[{'Dog'}],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: Empty set and SetView with one item",
        dict(
            setview=set(),
            others=[SetView({'Dog'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            others=[SetView({'Dog'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: Empty SetView and a string (iterable of chars)",
        dict(
            setview=SetView(set()),
            others=['Dog'],
            exp_result=SetView({'D', 'o', 'g'}),
        ),
        None, None, True
    ),
    (
        "union: Empty SetView and a list with one item",
        dict(
            setview=SetView(set()),
            others=[['Dog']],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),

    (
        "union: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            others=[set()],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "union: SetView with one item and a string (iterable of chars)",
        dict(
            setview=SetView({'Cat'}),
            others=['Dog'],
            exp_result=SetView({'Cat', 'D', 'o', 'g'}),
        ),
        None, None, True
    ),
    (
        "union: SetView with one single-char item and same string",
        dict(
            setview=SetView({'D'}),
            others=['D'],
            exp_result=SetView({'D'}),
        ),
        None, None, True
    ),
    (
        "union: SetView with one item and a list with same item",
        dict(
            setview=SetView({'Dog'}),
            others=[['Dog']],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),

    (
        "union: SetView with two items and set with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[{'Cat', 'Fish'}],
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "union: set with two items and SetView with one of them and "
        "one other",
        dict(
            setview={'Dog', 'Cat'},
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "union: SetView with two items and SetView with one of them "
        "and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog', 'Cat', 'Fish'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_UNION)
@simplified_test_function
def test_SetView_union(testcase, setview, others, exp_result):
    """
    Test function for SetView.union()
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview.union(*others)

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_SETVIEW_SUB = [

    # Testcases for SetView: self - other (= __sub__() / __rsub__())
    # Testcases for SetView: self -= other (= __isub__() / __sub__() + assign)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView (LHO) object to be used for the test.
    #   * other: Other object (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "sub: Empty SetView and an integer (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "sub: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            other={'Dog'},
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "sub: Empty set and SetView with one item",
        dict(
            setview=set(),
            other=SetView({'Dog'}),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "sub: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            other=SetView({'Dog'}),
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "sub: Empty SetView and a string (must be set or Set)",
        dict(
            setview=SetView(set()),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "sub: Empty SetView and a list (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "sub: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            other=set(),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "sub: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "sub: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "sub: SetView with one item and a string (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "sub: SetView with one item and a list (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "sub: SetView with two items and set with one of them and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other={'Cat', 'Fish'},
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "sub: set with two items and SetView with one of them and one other",
        dict(
            setview={'Dog', 'Cat'},
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "sub: SetView with two items and SetView with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_SUB)
@simplified_test_function
def test_SetView_sub(testcase, setview, other, exp_result):
    """
    Test function for SetView: self - other (= __sub__() / __rsub__())
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview - other

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_SUB)
@simplified_test_function
def test_SetView_isub(testcase, setview, other, exp_result):
    """
    Test function for SetView: self -= other (= __isub__() / __sub__() + assign)
    """

    # Don't change the testcase data, but a copy
    setview_copy = SetView(setview)
    setview_copy_id = id(setview_copy)

    # The code to be tested
    setview_copy -= other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `+=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __isub__() results in Python calling
    # __sub__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__isub__.
    # For SetView, the `-=` operator results in a new SetView object on a new
    # original set object.
    assert id(setview_copy) != setview_copy_id

    assert_equal(setview_copy, exp_result)


TESTCASES_SETVIEW_DIFFERENCE = [

    # testcases for setview.difference()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * other: Other object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "difference: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            others=[{'Dog'}],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "difference: Empty set and SetView with one item (emptiness checked "
        "before calling __rsub__)",
        dict(
            setview=set(),
            others=[SetView({'Dog'})],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "difference: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            others=[SetView({'Dog'})],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "difference: Empty SetView and a string (iterable of chars)",
        dict(
            setview=SetView(set()),
            others=['Dog'],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "difference: Empty SetView and a list with one item",
        dict(
            setview=SetView(set()),
            others=[['Dog']],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),

    (
        "difference: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            others=[set()],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "difference: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "difference: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "difference: SetView with one item and a string (iterable of chars)",
        dict(
            setview=SetView({'Cat'}),
            others=['Dog'],
            exp_result=SetView({'Cat'}),
        ),
        None, None, True
    ),
    (
        "difference: SetView with one single-char item and same string",
        dict(
            setview=SetView({'D'}),
            others=['D'],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "difference: SetView with one item and a list with same item",
        dict(
            setview=SetView({'Dog'}),
            others=[['Dog']],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),

    (
        "difference: SetView with two items and set with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[{'Cat', 'Fish'}],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "difference: set with two items and SetView with one of them and "
        "one other",
        dict(
            setview={'Dog', 'Cat'},
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "difference: SetView with two items and SetView with one of them "
        "and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_DIFFERENCE)
@simplified_test_function
def test_SetView_difference(testcase, setview, others, exp_result):
    """
    Test function for SetView.difference()
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview.difference(*others)

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_SETVIEW_XOR = [

    # Testcases for SetView: self ^ other (= __xor__() / __rxor__())
    # Testcases for SetView: self ^= other (= __ixor__() / __xor__() + assign)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView (LHO) object to be used for the test.
    #   * other: Other object (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "xor: Empty SetView and an integer (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "xor: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            other={'Dog'},
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: Empty set and SetView with one item",
        dict(
            setview=set(),
            other=SetView({'Dog'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            other=SetView({'Dog'}),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: Empty SetView and a string (must be set or Set)",
        dict(
            setview=SetView(set()),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "xor: Empty SetView and a list (must be set or Set)",
        dict(
            setview=SetView(set()),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "xor: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            other=set(),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            other=SetView(set()),
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "xor: SetView with one item and a string (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "xor: SetView with one item and a list (must be set or Set)",
        dict(
            setview=SetView({'Dog'}),
            other=['Dog'],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "xor: SetView with two items and set with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other={'Cat', 'Fish'},
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "xor: set with two items and SetView with one of them and "
        "one other",
        dict(
            setview={'Dog', 'Cat'},
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "xor: SetView with two items and SetView with one of them and "
        "one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            other=SetView({'Cat', 'Fish'}),
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_XOR)
@simplified_test_function
def test_SetView_xor(testcase, setview, other, exp_result):
    """
    Test function for SetView: self ^ other (= __xor__() / __rxor__())
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview ^ other

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_XOR)
@simplified_test_function
def test_SetView_ixor(testcase, setview, other, exp_result):
    """
    Test function for SetView: self ^= other (= __ixor__() / __xor__() + assign)
    """

    # Don't change the testcase data, but a copy
    setview_copy = SetView(setview)
    setview_copy_id = id(setview_copy)

    # The code to be tested
    setview_copy ^= other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the left hand object is a new object.
    # In Python, augmented assignment (e.g. `+=` is not guaranteed to
    # modify the left hand object in place, but can result in a new object.
    # Reason is that not implementing __ixor__() results in Python calling
    # __xor__() and assignment.
    # For details, see
    # https://docs.python.org/3/reference/datamodel.html#object.__ixor__.
    # For SetView, the `^=` operator results in a new SetView object on a new
    # original set object.
    assert id(setview_copy) != setview_copy_id

    assert_equal(setview_copy, exp_result)


TESTCASES_SETVIEW_SYMMETRIC_DIFFERENCE = [

    # Testcases for SetView.symmetric_difference()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    #   * other: Other object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "symmetric_difference: Empty SetView and an integer (must be iterable)",
        dict(
            setview=SetView(set()),
            others=[42],
            exp_result=None,
        ),
        TypeError, None, True
    ),

    (
        "symmetric_difference: Empty SetView and set with one item",
        dict(
            setview=SetView(set()),
            others=[{'Dog'}],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: Empty set and SetView with one item",
        dict(
            setview=set(),
            others=[SetView({'Dog'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: Empty SetView and SetView with one item",
        dict(
            setview=SetView(set()),
            others=[SetView({'Dog'})],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: Empty SetView and a string (iterable of chars)",
        dict(
            setview=SetView(set()),
            others=['Dog'],
            exp_result=SetView({'D', 'o', 'g'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: Empty SetView and a list with one item",
        dict(
            setview=SetView(set()),
            others=[['Dog']],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),

    (
        "symmetric_difference: SetView with one item and empty set",
        dict(
            setview=SetView({'Dog'}),
            others=[set()],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: set with one item and empty SetView",
        dict(
            setview={'Dog'},
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: SetView with one item and empty SetView",
        dict(
            setview=SetView({'Dog'}),
            others=[SetView(set())],
            exp_result=SetView({'Dog'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: SetView with one item and a string "
        "(iterable of chars)",
        dict(
            setview=SetView({'Cat'}),
            others=['Dog'],
            exp_result=SetView({'Cat', 'D', 'o', 'g'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: SetView with one single-char item and "
        "same string",
        dict(
            setview=SetView({'D'}),
            others=['D'],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: SetView with one item and a list with same item",
        dict(
            setview=SetView({'Dog'}),
            others=[['Dog']],
            exp_result=SetView(set()),
        ),
        None, None, True
    ),

    (
        "symmetric_difference: SetView with two items and set with one of them "
        "and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[{'Cat', 'Fish'}],
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: set with two items and SetView with one of them "
        "and one other",
        dict(
            setview={'Dog', 'Cat'},
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
    (
        "symmetric_difference: SetView with two items and SetView with one of "
        "them and one other",
        dict(
            setview=SetView({'Dog', 'Cat'}),
            others=[SetView({'Cat', 'Fish'})],
            exp_result=SetView({'Dog', 'Fish'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_SYMMETRIC_DIFFERENCE)
@simplified_test_function
def test_SetView_symmetric_difference(testcase, setview, others, exp_result):
    """
    Test function for SetView.symmetric_difference()
    """

    org_setview = SetView(setview)

    # The code to be tested
    result = setview.symmetric_difference(*others)

    # Verify the input SetView object has not changed
    assert_equal(setview, org_setview)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_SETVIEW_EQUAL = [

    # Testcases for SetView.__eq__(), __ne__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: SetView object #1 to use.
    #   * obj2: SetView object #2 to use.
    #   * exp_eq: Expected result of __eq__() and !__ne__()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Equal empty SetView with empty set",
        dict(
            obj1=SetView(set()),
            obj2=set(),
            exp_eq=True,
        ),
        None, None, True
    ),
    (
        "Equal empty SetView with empty SetView",
        dict(
            obj1=SetView(set()),
            obj2=SetView(set()),
            exp_eq=True,
        ),
        None, None, True
    ),

    (
        "Equal empty list with empty SetView",
        dict(
            obj1=[],
            obj2=SetView(set()),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal empty set with empty SetView",
        dict(
            obj1=set(),
            obj2=SetView(set()),
            exp_eq=True,
        ),
        None, None, True
    ),

    (
        "Equal empty SetView with set with one item",
        dict(
            obj1=SetView(set()),
            obj2=set('Cat'),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal empty SetView with SetView with one item",
        dict(
            obj1=SetView(set()),
            obj2=SetView({'Cat'}),
            exp_eq=False,
        ),
        None, None, True
    ),

    (
        "Equal SetView with one item with empty set",
        dict(
            obj1=SetView({'Cat'}),
            obj2=set(),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with empty SetView",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView(set()),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with set with different item",
        dict(
            obj1=SetView({'Dog'}),
            obj2=set('Cat'),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with SetView with different item",
        dict(
            obj1=SetView({'Dog'}),
            obj2=SetView({'Cat'}),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with set with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=set('Cat'),
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with SetView with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Cat'}),
            exp_eq=True,
        ),
        None, None, True
    ),

    (
        "Equal empty SetView with empty list",
        dict(
            obj1=SetView(set()),
            obj2=[],
            exp_eq=False,
        ),
        None, None, True
    ),
    (
        "Equal SetView with one item with list with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=['Cat'],
            exp_eq=False,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_EQUAL)
@simplified_test_function
def test_SetView_eq(testcase, obj1, obj2, exp_eq):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__eq__()
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
    TESTCASES_SETVIEW_EQUAL)
@simplified_test_function
def test_SetView_ne(testcase, obj1, obj2, exp_eq):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__ne__()
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


TESTCASES_SETVIEW_COMPARE_OPS = [

    # Testcases for SetView.__gt__(), __le__(),__lt__(), __ge__()

    # Note: Since sets are partially ordered, the testcases need to define
    # the expected results for all four comparison operations (as opposed to
    # being able to calculate two of them from the others).

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: SetView object #1 to use.
    #   * obj2: SetView object #2 to use.
    #   * exp_gt: Expected result of __gt__()
    #   * exp_lt: Expected result of __lt__()
    #   * exp_ge: Expected result of __ge__()
    #   * exp_le: Expected result of __le__()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Compare empty SetView with empty set",
        dict(
            obj1=SetView(set()),
            obj2=set(),
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare empty set with empty SetView",
        dict(
            obj1=set(),
            obj2=SetView(set()),
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with empty SetView",
        dict(
            obj1=SetView(set()),
            obj2=SetView(set()),
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),

    (
        "Compare empty SetView with set with one item",
        dict(
            obj1=SetView(set()),
            obj2={'Cat'},
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare empty set with SetView with one item",
        dict(
            obj1=set(),
            obj2=SetView({'Cat'}),
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with SetView with one item",
        dict(
            obj1=SetView(set()),
            obj2=SetView({'Cat'}),
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with empty set",
        dict(
            obj1=SetView({'Cat'}),
            obj2=set(),
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with empty SetView",
        dict(
            obj1={'Cat'},
            obj2=SetView(set()),
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with empty SetView",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView(set()),
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Cat'},
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with same item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Cat'}),
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Cat'}),
            exp_gt=False,
            exp_lt=False,
            exp_ge=True,
            exp_le=True,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Dog'},
            exp_gt=False,
            exp_lt=False,
            exp_ge=False,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with different item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Dog'}),
            exp_gt=False,
            exp_lt=False,
            exp_ge=False,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Dog'}),
            exp_gt=False,
            exp_lt=False,
            exp_ge=False,
            exp_le=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with two items with set with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2={'Dog'},
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare set with two items with SetView with one of them",
        dict(
            obj1={'Dog', 'Cat'},
            obj2=SetView({'Dog'}),
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with two items with SetView with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2=SetView({'Dog'}),
            exp_gt=True,
            exp_lt=False,
            exp_ge=True,
            exp_le=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with that item and one more",
        dict(
            obj1=SetView({'Dog'}),
            obj2={'Dog', 'Cat'},
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with that item and one more",
        dict(
            obj1={'Dog'},
            obj2=SetView({'Dog', 'Cat'}),
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with that item and one "
        "more",
        dict(
            obj1=SetView({'Dog'}),
            obj2=SetView({'Dog', 'Cat'}),
            exp_gt=False,
            exp_lt=True,
            exp_ge=False,
            exp_le=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_COMPARE_OPS)
@simplified_test_function
def test_SetView_gt(testcase, obj1, obj2, exp_gt, exp_lt, exp_ge, exp_le):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__gt__()
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
    TESTCASES_SETVIEW_COMPARE_OPS)
@simplified_test_function
def test_SetView_lt(testcase, obj1, obj2, exp_gt, exp_lt, exp_ge, exp_le):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__lt__()
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
    TESTCASES_SETVIEW_COMPARE_OPS)
@simplified_test_function
def test_SetView_ge(testcase, obj1, obj2, exp_gt, exp_lt, exp_ge, exp_le):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__ge__()
    """

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
    TESTCASES_SETVIEW_COMPARE_OPS)
@simplified_test_function
def test_SetView_le(testcase, obj1, obj2, exp_gt, exp_lt, exp_ge, exp_le):
    # pylint: disable=unused-argument
    """
    Test function for SetView.__le__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    le = (obj1 <= obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert le == exp_le


TESTCASES_SETVIEW_COMPARE_METH = [

    # Testcases for SetView.issuperset(), issubset()

    # Note: Since sets are partially ordered, the testcases need to define
    # the expected results for all four comparison operations (as opposed to
    # being able to calculate two of them from the others).

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: SetView object #1 to use.
    #   * obj2: SetView object #2 to use.
    #   * exp_issuperset: Expected result of issuperset()
    #   * exp_issubset: Expected result of issubset()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Compare empty SetView with empty set",
        dict(
            obj1=SetView(set()),
            obj2=set(),
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty set with empty SetView",
        dict(
            obj1=set(),
            obj2=SetView(set()),
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with empty SetView",
        dict(
            obj1=SetView(set()),
            obj2=SetView(set()),
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with empty list",
        dict(
            obj1=SetView(set()),
            obj2=[],
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty list with empty SetView (no issuperset())",
        dict(
            obj1=[],
            obj2=SetView(set()),
            exp_issuperset=None,
            exp_issubset=None,
        ),
        AttributeError, None, True
    ),

    (
        "Compare empty SetView with set with one item",
        dict(
            obj1=SetView(set()),
            obj2={'Cat'},
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty set with SetView with one item",
        dict(
            obj1=set(),
            obj2=SetView({'Cat'}),
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with SetView with one item",
        dict(
            obj1=SetView(set()),
            obj2=SetView({'Cat'}),
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare empty SetView with list with one item",
        dict(
            obj1=SetView(set()),
            obj2=['Cat'],
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with empty set",
        dict(
            obj1=SetView({'Cat'}),
            obj2=set(),
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with empty SetView",
        dict(
            obj1={'Cat'},
            obj2=SetView(set()),
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with empty SetView",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView(set()),
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with empty list",
        dict(
            obj1=SetView({'Cat'}),
            obj2=[],
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Cat'},
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with same item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Cat'}),
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Cat'}),
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with list with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=['Cat'],
            exp_issuperset=True,
            exp_issubset=True,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Dog'},
            exp_issuperset=False,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with different item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Dog'}),
            exp_issuperset=False,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Dog'}),
            exp_issuperset=False,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with list with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=['Dog'],
            exp_issuperset=False,
            exp_issubset=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with two items with set with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2={'Dog'},
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare set with two items with SetView with one of them",
        dict(
            obj1={'Dog', 'Cat'},
            obj2=SetView({'Dog'}),
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with two items with SetView with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2=SetView({'Dog'}),
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),
    (
        "Compare SetView with two items with list with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2=['Dog'],
            exp_issuperset=True,
            exp_issubset=False,
        ),
        None, None, True
    ),

    (
        "Compare SetView with one item with set with that item and one more",
        dict(
            obj1=SetView({'Dog'}),
            obj2={'Dog', 'Cat'},
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare set with one item with SetView with that item and one more",
        dict(
            obj1={'Dog'},
            obj2=SetView({'Dog', 'Cat'}),
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with SetView with that item and one "
        "more",
        dict(
            obj1=SetView({'Dog'}),
            obj2=SetView({'Dog', 'Cat'}),
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
    (
        "Compare SetView with one item with list with that item and one more",
        dict(
            obj1=SetView({'Dog'}),
            obj2=['Dog', 'Cat'],
            exp_issuperset=False,
            exp_issubset=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_COMPARE_METH)
@simplified_test_function
def test_SetView_issuperset(testcase, obj1, obj2, exp_issuperset, exp_issubset):
    # pylint: disable=unused-argument
    """
    Test function for SetView.issuperset()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    issuperset = obj1.issuperset(obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert issuperset == exp_issuperset


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_COMPARE_METH)
@simplified_test_function
def test_SetView_issubset(testcase, obj1, obj2, exp_issuperset, exp_issubset):
    # pylint: disable=unused-argument
    """
    Test function for SetView.issubset()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    issubset = obj1.issubset(obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert issubset == exp_issubset


TESTCASES_SETVIEW_ISDISJOINT = [

    # Testcases for SetView.isdisjoint()

    # Note: Since sets are partially ordered, the testcases need to define
    # the expected results for all four comparison operations (as opposed to
    # being able to calculate two of them from the others).

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: SetView object #1 to use.
    #   * obj2: SetView object #2 to use.
    #   * exp_isdisjoint: Expected result of isdisjoint()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Disjoint empty SetView with empty set",
        dict(
            obj1=SetView(set()),
            obj2=set(),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty set with empty SetView",
        dict(
            obj1=set(),
            obj2=SetView(set()),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty SetView with empty SetView",
        dict(
            obj1=SetView(set()),
            obj2=SetView(set()),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty SetView with empty list",
        dict(
            obj1=SetView(set()),
            obj2=[],
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty list with empty SetView (no issuperset())",
        dict(
            obj1=[],
            obj2=SetView(set()),
            exp_isdisjoint=None,
        ),
        AttributeError, None, True
    ),

    (
        "Disjoint empty SetView with set with one item",
        dict(
            obj1=SetView(set()),
            obj2={'Cat'},
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty set with SetView with one item",
        dict(
            obj1=set(),
            obj2=SetView({'Cat'}),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty SetView with SetView with one item",
        dict(
            obj1=SetView(set()),
            obj2=SetView({'Cat'}),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint empty SetView with list with one item",
        dict(
            obj1=SetView(set()),
            obj2=['Cat'],
            exp_isdisjoint=True,
        ),
        None, None, True
    ),

    (
        "Disjoint SetView with one item with empty set",
        dict(
            obj1=SetView({'Cat'}),
            obj2=set(),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint set with one item with empty SetView",
        dict(
            obj1={'Cat'},
            obj2=SetView(set()),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with empty SetView",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView(set()),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with empty list",
        dict(
            obj1=SetView({'Cat'}),
            obj2=[],
            exp_isdisjoint=True,
        ),
        None, None, True
    ),

    (
        "Disjoint SetView with one item with set with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Cat'},
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint set with one item with SetView with same item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Cat'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with SetView with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Cat'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with list with same item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=['Cat'],
            exp_isdisjoint=False,
        ),
        None, None, True
    ),

    (
        "Disjoint SetView with one item with set with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2={'Dog'},
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint set with one item with SetView with different item",
        dict(
            obj1={'Cat'},
            obj2=SetView({'Dog'}),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with SetView with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=SetView({'Dog'}),
            exp_isdisjoint=True,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with list with different item",
        dict(
            obj1=SetView({'Cat'}),
            obj2=['Dog'],
            exp_isdisjoint=True,
        ),
        None, None, True
    ),

    (
        "Disjoint SetView with two items with set with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2={'Dog'},
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint set with two items with SetView with one of them",
        dict(
            obj1={'Dog', 'Cat'},
            obj2=SetView({'Dog'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with two items with SetView with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2=SetView({'Dog'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with two items with list with one of them",
        dict(
            obj1=SetView({'Dog', 'Cat'}),
            obj2=['Dog'],
            exp_isdisjoint=False,
        ),
        None, None, True
    ),

    (
        "Disjoint SetView with one item with set with that item and one more",
        dict(
            obj1=SetView({'Dog'}),
            obj2={'Dog', 'Cat'},
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint set with one item with SetView with that item and one more",
        dict(
            obj1={'Dog'},
            obj2=SetView({'Dog', 'Cat'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with SetView with that item and one "
        "more",
        dict(
            obj1=SetView({'Dog'}),
            obj2=SetView({'Dog', 'Cat'}),
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
    (
        "Disjoint SetView with one item with list with that item and one more",
        dict(
            obj1=SetView({'Dog'}),
            obj2=['Dog', 'Cat'],
            exp_isdisjoint=False,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_ISDISJOINT)
@simplified_test_function
def test_SetView_isdisjoint(testcase, obj1, obj2, exp_isdisjoint):
    # pylint: disable=unused-argument
    """
    Test function for SetView.isdisjoint()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    isdisjoint = obj1.isdisjoint(obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isdisjoint == exp_isdisjoint


TESTCASES_SETVIEW_COPY = [

    # Testcases for SetView.copy()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "empty SetView",
        dict(
            setview=SetView(set()),
        ),
        None, None, True
    ),
    (
        "SetView of set with two items",
        dict(
            setview=SetView({'Dog', 'Cat'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_COPY)
@simplified_test_function
def test_SetView_copy(testcase, setview):
    """
    Test function for SetView.copy()
    """

    setview_set = setview._set  # pylint: disable=protected-access

    # The code to be tested
    setview_copy = setview.copy()

    setview_copy_set = setview_copy._set  # pylint: disable=protected-access

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the result type
    # pylint: disable=unidiomatic-typecheck
    assert type(setview_copy) is SetView

    # Verify the result is a different object than the SetView
    assert id(setview_copy) != id(setview)

    # Verify the new list is a different object than the original list,
    # if mutable
    if isinstance(setview_set, MutableSet):
        assert id(setview_copy_set) != id(setview_set)

    # Verify the new list has the same type as the original list
    # pylint: disable=unidiomatic-typecheck
    assert type(setview_copy_set) == type(setview_set)

    # Verify the new list is equal to the original list
    assert setview_copy_set == setview_set


def test_SetView_add():
    """
    Test function for the non-existing SetView.add()
    """
    setview = SetView({'a'})

    with pytest.raises(AttributeError):
        # The code to be tested
        setview.add('b')  # pylint: disable=no-member


def test_SetView_discard():
    """
    Test function for the non-existing SetView.discard()
    """
    setview = SetView({'a'})

    with pytest.raises(AttributeError):
        # The code to be tested
        setview.discard('a')  # pylint: disable=no-member


def test_SetView_remove():
    """
    Test function for the non-existing SetView.remove()
    """
    setview = SetView({'a'})

    with pytest.raises(AttributeError):
        # The code to be tested
        setview.remove('a')  # pylint: disable=no-member


def test_SetView_clear():
    """
    Test function for the non-existing SetView.clear()
    """
    setview = SetView({'a'})

    with pytest.raises(AttributeError):
        # The code to be tested
        setview.clear()  # pylint: disable=no-member


def test_SetView_pop():
    """
    Test function for the non-existing SetView.pop()
    """
    setview = SetView({'a'})

    with pytest.raises(AttributeError):
        # The code to be tested
        setview.pop()  # pylint: disable=no-member


TESTCASES_SETVIEW_PICKLE = [

    # Testcases for pickling and unpickling SetView objects

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * setview: SetView object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            setview=SetView(set()),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            setview=SetView({'Dog', 'Cat'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SETVIEW_PICKLE)
@simplified_test_function
def test_SetView_pickle(testcase, setview):
    """
    Test function for pickling and unpickling SetView objects
    """

    # Don't change the testcase data, but a copy
    setview_copy = SetView(setview)

    # Pickle the object
    pkl = pickle.dumps(setview_copy)

    del setview_copy

    # Unpickle the object
    setview2 = pickle.loads(pkl)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(setview2, setview)
