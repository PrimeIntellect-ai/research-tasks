You are a systems programmer tasked with fixing a broken build environment. 

In `/home/user/project`, there is a C++ project consisting of a test suite (`test_suite.cpp`) and multiple versions of a math library (in directories named `lib-1.5.2`, `lib-1.11.0`, and `lib-2.0.5`). 

Currently, the `Makefile` is broken in several ways:
1. **Semantic Versioning Logic:** The Makefile uses standard bash commands to dynamically pick the library directory to build, but its logic is flawed and selects an older version instead of the highest semantic version available.
2. **Shared Library Compilation:** It fails to build the shared library correctly (missing necessary compiler flags for shared objects).
3. **Linking:** It fails to link the `test_suite` executable against the generated shared library. The built executable must be able to run independently without needing `LD_LIBRARY_PATH` set.

Your task:
1. Fix the `Makefile` to correctly identify and use the highest semantic version directory (e.g., using bash built-ins or standard coreutils).
2. Fix the compilation instructions inside the `Makefile` so it correctly generates `libmathalg.so` from the selected directory's `mathalg.cpp`.
3. Fix the linking instructions inside the `Makefile` so `test_suite` links to `libmathalg.so` properly and sets the runtime library search path (rpath) to the current directory.
4. Do **not** modify `test_suite.cpp` or any of the `mathalg.cpp` files.
5. Run `make`.
6. Run the resulting executable `./test_suite` and redirect its standard output to `/home/user/project/test_result.log`.

If everything is correct, the unit tests inside `test_suite.cpp` will pass (they verify that the linked library is `>= 2.0.0` and that the math operations are correct).