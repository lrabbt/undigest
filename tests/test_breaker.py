import hashlib
import pytest

import undigest


@pytest.mark.parametrize(
    "original",
    [
        "1o",
        "zz",
        "lf0",
    ],
)
def test_sha256_break(original):
    # given
    original_length = len(original)
    digest = hashlib.sha256(original.encode("utf-8")).hexdigest()

    # when
    p = undigest.undigest(digest, original_length)

    # then
    assert p == original, "Wrong password"
