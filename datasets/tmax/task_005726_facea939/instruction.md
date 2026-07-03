You are a platform engineer maintaining a CI/CD pipeline for a Python project that requires a high-performance C extension. Recently, the pipeline started failing because the build system is linking against an outdated, incompatible version of a required shared library instead of the newer version.

Your task is to fix the pipeline by implementing semantic version resolution, writing the C extension, configuring the build, and orchestrating an end-to-end test.

Here are your specific requirements:

**Phase 1: Library Preparation**
1. In `/home/user/libs`, create two C files:
   - `libmagic_v1.1.5.c` which contains a function `int get_magic_number()` returning `42`.
   - `libmagic_v2.3.1.c` which contains a function `int get_magic_number()` returning `99`.
2. Compile both of these C files into shared objects (`.so`) in the directory `/home/user/libs/bin`. They should be named `libmagic_v1.1.5.so` and `libmagic_v2.3.1.so` respectively. 

**Phase 2: Semantic Version Resolution**
1. Write a Python script at `/home/user/resolve.py` that acts as a version resolver.
2. The script should take two command-line arguments: a directory path and a minimum semantic version string (e.g., `2.0.0`).
3. It must scan the given directory for files matching `libmagic_v<version>.so`.
4. Using Python (you may use the standard `packaging` or `distutils` library, or write a custom parser), find the library with the highest semantic version that is strictly greater than or equal to the minimum version provided.
5. The script must print *only* the absolute path to the chosen `.so` file to standard output.

**Phase 3: Minimal Program Construction & Build System Linking**
1. In `/home/user/project`, write a minimal Python C-extension named `magic_ext.c`. It must define a Python module `magic_ext` containing a single function `get_value()` that calls the external C function `get_magic_number()` and returns its result as a Python integer.
2. Write a `/home/user/project/setup.py` build script.
3. The `setup.py` script must programmatically call your `/home/user/resolve.py` script, passing `/home/user/libs/bin` and `2.0.0` as arguments.
4. It must capture the output path and configure the `Extension` object to dynamically link against that exact shared library. Note: you may need to use `extra_objects`, `extra_link_args`, or set the `rpath` appropriately so the library can be found at runtime.
5. Build the extension in-place in `/home/user/project`.

**Phase 4: End-to-End Test Orchestration**
1. Write an end-to-end test script at `/home/user/project/test_e2e.py`.
2. This script must import the newly built `magic_ext` module, call `magic_ext.get_value()`, and assert that the returned value is `99`.
3. If the assertion passes, the script must create a log file at `/home/user/result.log` containing exactly the string: `E2E SUCCESS: 99`.

Ensure all files are created with appropriate permissions. You are expected to run the final test script to generate `/home/user/result.log`.