#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from random import Random

ct = Path('ct.bin').read_bytes()

for i in range(0, 1000000):
    r = Random(str(datetime(2021, 2, 23, 22, 8, 44, i)))
    rb = r.randbytes(32)
    pt = bytes([a ^ b for a, b in zip(rb, ct)])
    if pt.startswith(b'flag'):
        print(pt.decode())
        exit()
