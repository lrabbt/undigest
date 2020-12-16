#!/usr/bin/env python

from xmlrpc.client import ServerProxy

import sys


server_host = sys.argv[1]
nprocs = int(sys.argv[2])
hexdigest = sys.argv[3]
original_size = int(sys.argv[4])

s = ServerProxy(server_host)
undigested = s.undigest(nprocs, hexdigest, original_size)
print(f'Undigested: "{undigested}"')
