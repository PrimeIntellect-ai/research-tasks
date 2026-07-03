You are a release manager preparing a critical data-processing module for deployment. The module consists of a performance-critical C extension loaded by a Python wrapper. 

Currently, the build system is broken, and the previous developer left a severe memory leak in the C code that causes the Python deployment to consume too much memory over time.

Your tasks are:
1. **Fix the Makefile**: Located at `/home/user/build/Makefile`. The `release` target is supposed to compile `crunch.c` into a shared library named `libcrunch.so` with `-O3` optimization, but it currently lacks the necessary flags to create a shared library (it fails to build or builds an invalid binary). Fix the `release` target so that running `make release` successfully produces a valid `libcrunch.so`.
2. **Fix the Memory Leak**: The C source code is at `/home/user/build/crunch.c`. Find the memory leak in the `process_array` function and fix it.
3. **Verify via Python**: A Python script `/home/user/build/test_run.py` tests the extension. When you run it, it should complete successfully without exhausting memory.
4. **Generate a Release Report**: Once the Makefile and C code are fixed, compile the release build (`make release`), verify it runs cleanly, and then create a file named `/home/user/release_info.txt`. The file must contain exactly two lines:
   - Line 1: The exact string `BUILD: SUCCESS`
   - Line 2: The exact string `LEAK: FIXED`

Constraints:
- Do not modify `test_run.py`.
- Ensure your fixed C code frees any dynamically allocated memory it uses before returning.