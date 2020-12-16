#!/usr/bin/env python

from xmlrpc.client import ServerProxy

import matplotlib.pyplot as plt
import numpy as np

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
    nprocs_list = [1, 2, 4, 8, 12, 16, 20, 24]
    num_requests = 5
    msg_size = 4

    first_throughput = None
    throughput_list = []
    speedup_list = []
    for nprocs in nprocs_list:
        s = time.perf_counter()
        r = asyncio.run(evaluate_requests(url, nprocs, num_requests, msg_size))
        elapsed = r["elapsed"]
        throughput = r["throughput"]

        if first_throughput is None:
            first_throughput = throughput
        speedup = throughput / first_throughput

        throughput_list.append(throughput)
        speedup_list.append(speedup)

    plt_x = np.array(nprocs_list)
    plt_y = np.array(throughput_list)

    ax = plt.subplot(211)
    (t_line,) = ax.plot(plt_x, plt_y, "bo-", label="throughput")
    ax.set_xlabel("nprocs")
    ax.set_ylabel("throughput (req/s)")
    ax.set_title("Throughput")

    for x, y in zip(plt_x, plt_y):
        label = f"{y:.2f}"

        plt.annotate(
            label, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    ax2 = plt.subplot(212)

    plt_y2 = np.array(speedup_list)

    (s_line,) = ax2.plot(plt_x, plt_y2, "bo-", label="speedup", color="red")
    ax2.set_xlabel("nprocs")
    ax2.set_ylabel("speedup")
    ax2.set_title("Speedup")

    for x, y in zip(plt_x, plt_y2):
        label = f"{y:.2f}"

        plt.annotate(
            label, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    plt.show()


if __name__ == "__main__":
    main()
