#!/usr/bin/env python

import hashlib
import sys


original = sys.argv[1]
print(hashlib.sha256(original.encode("utf-8")).hexdigest())
