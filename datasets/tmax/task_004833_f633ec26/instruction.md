You are a platform engineer responsible for maintaining our C-based CI/CD pipelines. Our latest nightly build for the "PolyHash" mathematical encoding library has failed due to compilation errors, shared library linkage issues, and failing memory checks.

The PolyHash library takes an ASCII string and calculates a polynomial hash. Each character's ASCII integer value is used as a coefficient in a polynomial, evaluated at a given integer $x$. 

The project is located at `/home/user/polybuild`.

Your objectives are:
1. **Fix the Build System**: The `Makefile` in `/home/user/polybuild` is broken. It fails to correctly compile `src/polyhash.c` into a position-independent shared library (`libpolyhash.so`) and fails to link it correctly to the `test_runner`. Repair the `Makefile` so that running `make` successfully builds `libpolyhash.so` and `test_runner` without errors.
2. **Fix the Memory Leak**: The CI/CD pipeline caught a memory leak in `src/polyhash.c`. Use a memory profiler to identify and fix the leak in the C code.
3. **Generate Valgrind Report**: Run the compiled `test_runner` through Valgrind to prove the memory leak is resolved. Save the exact standard error output of Valgrind to `/home/user/polybuild/valgrind.log`.
4. **Generate Output**: Ensure the `test_runner` executes successfully. It evaluates the string `"CI_CD_SUCCESS"` at $x = 3$. Have it write the final integer result to `/home/user/polybuild/result.txt`.

Ensure your fixes leave the code functionally correct (the mathematical logic is sound, only the memory management and build configurations are flawed). Do not change the mathematical algorithm.

When you are done, the following files must exist and be correct:
- `/home/user/polybuild/libpolyhash.so` (valid shared object library)
- `/home/user/polybuild/valgrind.log` (showing 0 bytes definitely lost)
- `/home/user/polybuild/result.txt` (containing the correct numeric hash output)