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
