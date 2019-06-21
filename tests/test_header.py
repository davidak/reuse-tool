# SPDX-Copyright: 2019 Free Software Foundation Europe e.V.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""All tests for reuse.header"""

from inspect import cleandoc

import pytest

from reuse import SpdxInfo
from reuse._comment import CommentCreateError
from reuse.header import create_header, find_and_replace_header

# pylint: disable=implicit-str-concat-in-sequence


def test_create_header_simple():
    """Create a super simple header."""
    spdx_info = SpdxInfo(
        set(["GPL-3.0-or-later"]), set(["SPDX" "-Copyright: Mary Sue"])
    )
    expected = cleandoc(
        """
        # spdx-Copyright: Mary Sue
        #
        # spdx-License-Identifier: GPL-3.0-or-later
        """
    ).replace("spdx", "SPDX")

    assert create_header(spdx_info) == expected


def test_create_header_already_contains_spdx():
    """Create a new header from a header that already contains SPDX info."""
    spdx_info = SpdxInfo(
        set(["GPL-3.0-or-later"]), set(["SPDX" "-Copyright: Mary Sue"])
    )
    existing = cleandoc(
        """
        # spdx-Copyright: John Doe
        #
        # spdx-License-Identifier: MIT
        """
    ).replace("spdx", "SPDX")
    expected = cleandoc(
        """
        # spdx-Copyright: John Doe
        # spdx-Copyright: Mary Sue
        #
        # spdx-License-Identifier: GPL-3.0-or-later
        # spdx-License-Identifier: MIT
        """
    ).replace("spdx", "SPDX")

    assert create_header(spdx_info, header=existing) == expected


def test_create_header_existing_is_wrong():
    """If the existing header contains errors, raise a CommentCreateError."""
    spdx_info = SpdxInfo(
        set(["GPL-3.0-or-later"]), set(["SPDX" "-Copyright: Mary Sue"])
    )
    existing = cleandoc(
        """
        # spdx-Copyright: John Doe
        #
        # spdx-License-Identifier: MIT AND OR 0BSD
        """
    ).replace("spdx", "SPDX")

    with pytest.raises(CommentCreateError):
        create_header(spdx_info, header=existing)


def test_find_and_replace_no_header():
    """Given text without header, add a header."""
    spdx_info = SpdxInfo(
        set(["GPL-3.0-or-later"]), set(["SPDX" "-Copyright: Mary Sue"])
    )
    text = "pass"
    expected = cleandoc(
        """
        # spdx-Copyright: Mary Sue
        #
        # spdx-License-Identifier: GPL-3.0-or-later

        pass
        """
    ).replace("spdx", "SPDX")

    assert find_and_replace_header(text, spdx_info) == expected


def test_find_and_replace_verbatim():
    """Replace a header with itself."""
    spdx_info = SpdxInfo(set(), set())
    text = cleandoc(
        """
        # spdx-Copyright: Mary Sue
        #
        # spdx-License-Identifier: GPL-3.0-or-later

        pass
        """
    ).replace("spdx", "SPDX")

    assert find_and_replace_header(text, spdx_info) == text