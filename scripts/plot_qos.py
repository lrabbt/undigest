#!/usr/bin/env python

from xmlrpc.client import ServerProxy

import matplotlib.pyplot as plt
import numpy as np

import hashlib
import time
import sys


def make_msg(size):
    msg = ""
    for _ in range(size):
        msg += "z"
    return msg


def main():
    url = sys.argv[1]
    msg_size = 4
    nprocs_list = [1, 2, 4, 8, 12, 16, 20, 24]
    msg = make_msg(msg_size)
    digest = hashlib.sha256(msg.encode("utf-8")).hexdigest()

    elapsed_times = []
    for nprocs in nprocs_list:
        start = time.perf_counter()
        with ServerProxy(url) as s:
            s.undigest(nprocs, digest, msg_size)
        elapsed = time.perf_counter() - start
        elapsed_times.append(elapsed)

    plt_x = np.array(nprocs_list)
    plt_y = np.array(elapsed_times)

    fig, ax = plt.subplots()
    ax.plot(plt_x, plt_y, "bo-", label="Elapsed time")
    ax.set_xlabel("nprocs")
    ax.set_ylabel("elapsed time (seconds)")
    ax.set_title("Elapsed time")

    for x, y in zip(plt_x, plt_y):
        label = f"{y:.2f}"

        plt.annotate(
            label, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    plt.show()


if __name__ == "__main__":
    main()
