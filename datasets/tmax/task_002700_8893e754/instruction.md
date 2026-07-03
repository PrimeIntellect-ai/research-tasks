You are tasked with migrating a mathematical library interface from Python 2 to Python 3. The workspace is located at `/home/user/math_migration`. You will need to fix a build process, use FFI to interface with C code, write property-based tests, and implement a semantic version check in bash.

Please complete the following steps:

1. **Fix the Makefile**: The `/home/user/math_migration/Makefile` is broken (likely due to incorrect indentation and missing compiler flags for shared libraries). Fix it so that running `make` successfully compiles `/home/user/math_migration/mathops.c` into a shared library named `libmathops.so`.

2. **Cross-Language Interop (FFI)**: Write a Python 3 test script `/home/user/math_migration/test_mathops.py` that uses the `ctypes` library to load `libmathops.so`. Expose the C functions `add_safe(int, int)` and `multiply_safe(int, int)`. 

3. **Property-Based Testing**: Inside `test_mathops.py`, write property-based tests using the `hypothesis` library (you may need to install it, along with `pytest`). Test that your wrapper functions for `add_safe` and `multiply_safe` produce the exact same results as native Python `+` and `*` operators for any integer between `-1000` and `1000`. Run your tests using `pytest` and redirect the standard output to `/home/user/math_migration/pytest_results.log`.

4. **Semantic Version Comparison**: The C library exposes a function `const char* get_version()` which returns a semantic version string. Write a bash script `/home/user/math_migration/check_version.sh` that:
   - Evaluates a short inline Python snippet to call `get_version()` via `ctypes` and prints the version string.
   - Captures this version string in bash.
   - Uses standard coreutils (specifically `sort -V`) to semantically compare the extracted version against `"2.0.0"`.
   - If the extracted version is greater than or equal to `"2.0.0"`, the script must write the string `"VERSION_OK"` to `/home/user/math_migration/version.log`. Otherwise, it must write `"VERSION_TOO_OLD"`.
   
Execute `./check_version.sh` so that `/home/user/math_migration/version.log` is created.