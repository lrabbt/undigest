from xmlrpc.server import SimpleXMLRPCServer

from undigest import distributed_undigest

import logging

logger = logging.getLogger(__name__)


def main(host="localhost", port=8000, log_level="INFO", *args, **kwargs):
    logging.basicConfig(level=logging.getLevelName(log_level))

    with SimpleXMLRPCServer((host, port), allow_none=True) as server:
        server.register_introspection_functions()

        server.register_function(distributed_undigest, "undigest")

        server.serve_forever()


if __name__ == "__main__":
    main()
