You are a systems programmer working on a C application that depends on two dynamic libraries (`libalpha` and `libbeta`). The project is located in `/home/user/project`. 

Currently, the project is failing to build and run correctly due to a combination of Makefile misconfigurations and a memory safety bug (Undefined Behavior) in the semantic version parsing logic.

Your tasks are:

1. **Fix the Makefile:**
   The `Makefile` in `/home/user/project/` currently fails to build an executable that can run standalone. It compiles, but running `./app` results in a shared library loading error because the libraries are in `/home/user/project/libs/`. 
   Modify the `Makefile` so that `app` successfully links to `libalpha` and `libbeta`, and can find them at runtime *without* relying on the `LD_LIBRARY_PATH` environment variable being set globally (hint: use the linker's rpath feature). The executable must be named `app`.

2. **Fix the Memory Safety Bug in `app.c`:**
   The main program relies on a custom semantic versioning comparison function `compare_semver(const char* v1, const char* v2)` to check if the loaded `libalpha` meets the minimum version requirement of `2.1.0`. 
   Currently, `app.c` contains a dangerous memory safety vulnerability (buffer overflow) in this function that causes a segmentation fault when longer version strings are evaluated. Refactor `compare_semver` to be memory-safe. It should correctly parse versions like "X.Y.Z" and return `>0` if `v1 > v2`, `0` if `v1 == v2`, and `<0` if `v1 < v2`.

3. **Write an Automated Test:**
   Create a Python test script at `/home/user/project/test.py` that executes the `./app` binary using the `subprocess` module.
   `app` optionally takes a version string as its first CLI argument to override the library's reported version.
   The script must:
   - Run `./app 2.1.5` and assert that the exit code is `0`.
   - Run `./app 1.9.0` and assert that the exit code is `1`.
   - Run `./app 10.20.30` and assert that the exit code is `0`.
   If all tests pass, the script should print `ALL TESTS PASSED`.

4. **Generate Verification Log:**
   Once everything is fixed, run `./app` (with no arguments) and redirect its standard output to `/home/user/project/success.log`.

Make sure you do not change the function signatures of `get_alpha_version` or `beta_init` exported by the shared libraries.