import hashlib
import logging
import tempfile

from sucuri import Source, Serializer, DFGraph, Scheduler, FilterTagged


logger = logging.getLogger(__name__)

DEFAULT_CHARACTERS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz" + "0123456789"
)


def undigest(
    digest: str,
    original_size: int,
    valid_characters: str = DEFAULT_CHARACTERS,
    original_base: str = "",
):
    """Undigest some hexdigest string. The original string size mut be passed."""
    return _try_password(original_base, 0, valid_characters, original_size, digest)


def _try_password(
    password: str, pos: int, chars: str, psize: int, expected_digest: str
):
    """Tries all combinations from pos onwards."""
    if pos == psize:
        byte_pass = password.encode("utf-8")
        digest = hashlib.sha256(byte_pass).hexdigest()
        if digest == expected_digest:
            return password
        else:
            return None
    else:
        for c in chars:
            p = password + c
            found = _try_password(p, pos + 1, chars, psize, expected_digest)
            if found:
                return found
        return None


def _try_password_wrapper(args):
    """Wrapper around _try_password to be used by sucuri."""
    arg = args[0]
    logger.debug(arg)
    return _try_password(*arg)


def distributed_undigest(
    nprocs: int,
    digest: str,
    original_size: int,
    valid_characters: str = DEFAULT_CHARACTERS,
):
    """Undigest hexdigest using distributed processes."""

    feeder_data = []
    for c in valid_characters:
        feeder_data.append([c, 1, valid_characters, original_size, digest])

    with tempfile.NamedTemporaryFile() as tmp_file:
        serialize_undigest = generate_undigest_serializer(tmp_file.name)

        graph = DFGraph()
        sched = Scheduler(graph, nprocs, mpi_enabled=False)

        feed_first_char = Source(feeder_data)
        find_undigested = FilterTagged(_try_password_wrapper, 1)
        undigested = Serializer(serialize_undigest, 1)

        graph.add(feed_first_char)
        graph.add(find_undigested)
        graph.add(undigested)

        feed_first_char.add_edge(find_undigested, 0)
        find_undigested.add_edge(undigested, 0)

        sched.start()

        found_undigested = tmp_file.read().strip().decode("utf-8")
        logger.debug(found_undigested)
        return found_undigested


def generate_undigest_serializer(filepath):
    """Generates serializer with file for communication with main process."""

    def serialize_undigest(args):
        """Filters out all procs return values and lets only found undigested string."""
        found = args[0]
        if found:
            print(f'Original string: "{found}"')
            with open(filepath, "w") as f:
                f.write(found)

    return serialize_undigest
