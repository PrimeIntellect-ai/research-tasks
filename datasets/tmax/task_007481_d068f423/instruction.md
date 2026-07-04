You are a systems programmer dealing with a broken web security token parser. The parser is written in C and loaded into a Python backend using `ctypes`. 

Currently, your team is experiencing two major issues in the `/home/user/workspace` directory:
1. **Linking Issue**: The `Makefile` is improperly configured. Running `make` does not produce a valid shared object that Python can load. Running `python3 test.py` currently results in an `OSError: invalid ELF header` or similar loading error.
2. **Memory Safety Issue**: The C parser (`parser.c`) implements a state machine to parse token fields (`KEY:VALUE;`), but it lacks bounds checking. A maliciously crafted long token causes a buffer overflow and a segmentation fault.

Your tasks:
1. Fix the `Makefile` in `/home/user/workspace` so that `make` successfully compiles `parser.c` into a valid shared library named `libparser.so`.
2. Fix the memory safety bug in `parser.c`. The buffers for `key` and `value` are exactly 16 bytes long. Modify the state machine to truncate any keys or values that exceed 15 characters (leaving room for the null terminator), discarding the excess characters until the next delimiter (`:` or `;`).
3. Run `make`.
4. Run `python3 /home/user/workspace/test.py`. This script feeds a malicious payload to the library. If your fixes are correct, it will safely execute without segfaulting and write the parsed key-value pairs to `/home/user/workspace/result.json`.

Ensure that `/home/user/workspace/result.json` is generated and contains the safely truncated output.