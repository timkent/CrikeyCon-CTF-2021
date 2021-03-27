# Back in time

## What we know

- It's a beginner crypto challenge
- It's called "Back in time"
- It comes in a zipfile, containing the `encrypt.py` script and the generated ciphertext in `ct.bin`
- The flag format for this CTF (CrikeyCon 2021) begins with `flag`

## Archive contents

```zsh
% unzip encrypt.zip
Archive:  encrypt.zip
  inflating: encrypt.py
 extracting: ct.bin
```

## Script contents

```python
#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from random import Random

flag = input().encode()

r = Random(str(datetime.now()))

rb = r.randbytes(32)
ct = bytes([a ^ b for a, b in zip(rb, flag)])

Path('ct.bin').write_bytes(ct)
```

The script asks for the flag as input, creates some random bytes, and performs an `XOR` operation using these random bytes against the flag input. It then writes the result to the file `ct.bin`.

If you are new to Python you may find the list comprehension syntax confusing, but basically we are iterating over each byte of the random bytes and flag, performing an `XOR`, and assembling the result into a byte array. One extra detail here is the flag must be less than 32 bytes (the length of `rb`) or it will be truncated due to the way `zip()` operates.

So we have the ciphertext, and to recover the plaintext (flag) we need to undo the `XOR` operation. As with any symmetric encryption, having the ciphertext and the key used for encryption would give us everything we need!

If we have a look at how `Random` is instantiated, a seed value of `str(datetime.now())` is provided, and looking at the documentation for `Random` states that it is deterministic, so giving the same seed would provide the same random bytes each time we run the program!

Let's see what a seed should look like:

```python
>>> str(datetime.now())
'2021-03-27 18:12:29.783365'
```

## Solution

How do we seed `Random` with the same value that was used for encryption? By reading the timestamps of `ct.bin`:

```zsh
% stat ct.bin
16777221 2642938 -rw-r--r-- 1 tim staff 0 32 "Feb 23 22:21:31 2021" "Feb 23 22:08:44 2021" "Feb 23 22:08:44 2021" "Feb 23 22:08:44 2021" 4096 8 0 ct.bin
```

As we only have seconds precision on our timestamp we'll have to brute force the microseconds, but this isn't a great deal of work (in fact you could do the same with seconds and still have a result in a reasonable amount of time). We know what the flag should look like, so we can bail as soon as we get back a valid bytestring:

```python
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
```

Here we go, solved in under 15 seconds:

```
% time ./solve.py
flag{it_started_with_a_bad_seed}
./solve.py  14.78s user 0.02s system 99% cpu 14.817 total
```
