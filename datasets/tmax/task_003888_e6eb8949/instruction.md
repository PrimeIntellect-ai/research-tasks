I need you to fix and optimize a vendored C library so that we can use it in a minimal container environment.

We have a custom C library for serialization and checksum calculation located at `/app/libfastcrc`. This library was intended to be built as a shared object (`libfastcrc.so`) and called from a Python wrapper. However, the build is currently broken due to a faulty Makefile (missing PIC flags, incorrect linking, and wrong environment variables). 

Your task:
1. Fix the Makefile in `/app/libfastcrc` so that running `make` successfully produces `libfastcrc.so`.
2. Ensure the shared library properly exports the `compute_checksum_and_serialize` function, which takes a byte array and its length, and returns a 32-bit checksum.
3. Optimize the C implementation if necessary. The library must be highly performant.
4. We have a test script at `/app/benchmark.py` which loads your built `libfastcrc.so` and compares its performance against a reference Python implementation. Your fixed and compiled C library must achieve a runtime speedup of at least 15x over the Python reference.

Please leave the resulting compiled shared library at `/app/libfastcrc/libfastcrc.so` so our verification script can benchmark it. Do not modify `/app/benchmark.py`.