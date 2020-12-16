#!/usr/bin/env python

from xmlrpc.client import ServerProxy

import hashlib
import asyncio
import time
import sys


def make_msg(size):
    msg = ""
    for _ in range(size):
        msg += "z"
    return msg


async def make_request(url, *args, **kwargs):
    with ServerProxy(url) as s:
        return s.undigest(*args, **kwargs)


async def evaluate_requests(url, nprocs, num_requests, msg_size):
    msg = make_msg(msg_size)
    digest = hashlib.sha256(msg.encode("utf-8")).hexdigest()

    urequests = []
    for i in range(num_requests):
        urequests.append(make_request(url, nprocs, digest, msg_size))

    start = time.perf_counter()
    await asyncio.gather(*urequests)
    elapsed = time.perf_counter() - start
    throughput = num_requests / elapsed

    return {
        "elapsed": elapsed,
        "throughput": throughput,
    }


def main():
    url = sys.argv[1]
    nprocs = int(sys.argv[2])
    num_requests = int(sys.argv[3])
    msg_size = int(sys.argv[4])

    s = time.perf_counter()
    r = asyncio.run(evaluate_requests(url, nprocs, num_requests, msg_size))
    elapsed = r["elapsed"]
    throughput = r["throughput"]

    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    print(f"{__file__} throughput is {throughput:0.2f}req/s")


if __name__ == "__main__":
    main()
