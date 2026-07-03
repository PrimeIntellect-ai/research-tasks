You are a systems programmer debugging a C library that calculates error-correcting checksums. You have written a Python wrapper using `ctypes` to interface with this library, but you are running into a few issues.

In your workspace `/home/user/`, you have three files:
1. `crc_algo.c`: Contains the core logic for calculating a CRC32 checksum. It allocates a temporary buffer internally for processing.
2. `wrapper.c`: Provides the FFI boundary for the Python script.
3. `test.py`: A Python script that loads the shared library and calculates the checksum for the string `"ALGORITHMIC_DEBUGGING"`.

Currently, running `python3 /home/user/test.py` fails with a library linking issue:
`OSError: /home/user/libwrapper.so: undefined symbol: custom_crc`

Furthermore, it is suspected that even when linked correctly, the C algorithm contains a memory error (an out-of-bounds read) that causes non-deterministic checksum outputs depending on the state of the heap. 

Your tasks are:
1. Fix the `undefined symbol` linking issue so that `libwrapper.so` can be loaded by Python. You will need to recompile the shared library.
2. Locate and fix the memory out-of-bounds bug in `/home/user/crc_algo.c` so the checksum is deterministic and only processes the exact bytes of the input.
3. Once fixed and recompiled, run `test.py`. Take the integer checksum it outputs and save it to a file exactly at `/home/user/checksum_result.txt`.

Ensure your final compiled library is located at `/home/user/libwrapper.so`. You may use `valgrind` or any standard debugging utilities if needed.