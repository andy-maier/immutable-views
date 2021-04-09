"""
Test import and versioning of the package.
"""


def test_import():
    """
    Test import of the package.
    """
    # pylint: disable=import-outside-toplevel
    import immutable_views  # noqa: F401
    assert immutable_views


def test_versioning():
    """
    Test import of the package.
    """
    # pylint: disable=import-outside-toplevel
    import immutable_views  # noqa: F401
    assert immutable_views.__version__
