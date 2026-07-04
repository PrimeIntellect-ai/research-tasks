You are tasked with fixing a broken Python-C hybrid project located in `/home/user/collatz_ext`.

The project implements a fast mathematical computation for the Collatz conjecture sequence length using a C shared library (`libcollatz.so`), which is then loaded and tested via Python's `ctypes` module.

Currently, the project is completely broken:
1. The `Makefile` has linking/compilation errors and fails to produce a valid shared object (`libcollatz.so`).
2. Even if compiled, the underlying C implementation in `collatz.c` contains a mathematical logic bug that causes infinite loops or incorrect results, failing the Python unit tests.

Your objectives are:
1. Fix the `Makefile` so that running `make` successfully compiles `collatz.c` into a valid shared library `libcollatz.so` (ensure proper Position Independent Code and shared flags).
2. Analyze and debug the C code in `collatz.c`. Fix the mathematical logic bug so it correctly computes the number of steps to reach `1` for any positive integer `n` according to the Collatz conjecture. (If `n=1`, the length is `0`).
3. Use the Python end-to-end test orchestration script `run_tests.py` to compile and run the Python unit tests (`test_collatz.py`). Ensure all tests pass.
4. Once everything passes, manually calculate the Collatz sequence length for `n = 27` using the fixed library.
5. Create a final report file at `/home/user/collatz_ext/fix_report.txt`. The file must contain exactly two lines:
   - Line 1: The exact word `SUCCESS`
   - Line 2: The integer length of the Collatz sequence for `n = 27`.

You can use any bash tools, python scripts, or C debugging techniques you see fit.