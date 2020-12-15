import hashlib


DEFAULT_CHARACTERS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz" + "0123456789"
)


def undigest(
    digest: str,
    original_size: int,
    valid_characters: str = DEFAULT_CHARACTERS,
):
    """Undigest some hexdigest string. The original string size mut be passed."""
    return _try_password("", 0, valid_characters, original_size, digest)


def _try_password(
    password: str, pos: int, chars: str, psize: int, expected_digest: str
):
    """Tries all combinations from pos onwards."""
    if pos == psize - 1:
        for c in chars:
            p = password + c
            byte_pass = p.encode("utf-8")
            digest = hashlib.sha256(byte_pass).hexdigest()
            if digest == expected_digest:
                return p
        return None
    else:
        for c in chars:
            p = password + c
            found = _try_password(p, pos + 1, chars, psize, expected_digest)
            if found:
                return found
        return None
