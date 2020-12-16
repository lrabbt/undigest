import hashlib
import pytest

import undigest


EXAMPLE_STRINGS = [
    "1o",
    "zz",
    "lf0",
]


@pytest.mark.parametrize("original", EXAMPLE_STRINGS)
def test_sha256_break(original):
    # given
    original_length = len(original)
    digest = hashlib.sha256(original.encode("utf-8")).hexdigest()

    # when
    p = undigest.undigest(digest, original_length)

    # then
    assert p == original, "Wrong password"


@pytest.mark.parametrize("original", EXAMPLE_STRINGS)
@pytest.mark.parametrize("nprocs", [1, 2, 4])
def test_sha256_parallel_break(original, nprocs, capfd):
    # given
    original_length = len(original)
    digest = hashlib.sha256(original.encode("utf-8")).hexdigest()

    # when
    response = undigest.distributed_undigest(nprocs, digest, original_length)

    # then
    assert response == original, "Wrong password"
