I have a messy project repository in `/home/user/project` that consists of a C data processing library and a Python test suite. Currently, all files are dumped in the root directory, the Makefile is broken, the C code has a memory leak, and the Python test suite is missing a fixture to load the shared library.

I need you to organize the project and fix the code according to the following constraints:

1. **File Organization (Constraint Satisfaction):**
   - Create directories: `/home/user/project/src`, `/home/user/project/tests`, and `/home/user/project/build`.
   - Move `processor.c` and `processor.h` into the `src/` directory.
   - Move `test_processor.py` into the `tests/` directory.

2. **Build System Configuration:**
   - Modify the `Makefile` in `/home/user/project` so that running `make` compiles `src/processor.c` into a shared library located exactly at `/home/user/project/build/libprocessor.so`.
   - The compilation must include the `-fPIC` and `-shared` flags.
   - Ensure the `clean` target removes the `build/` directory contents.

3. **Test Fixture Setup:**
   - Edit `/home/user/project/tests/test_processor.py`.
   - Add a `setUp` method in the `TestProcessor` class that uses Python's `ctypes` to load the shared library from `../build/libprocessor.so`.
   - The test function `test_process` is already written but relies on `self.lib` being set to the loaded shared library.

4. **Memory Debugging:**
   - The `processor.c` code contains a memory leak in the `process_data` function. It allocates a buffer that it never frees.
   - Fix the C code to free the allocated memory properly.
   - After fixing it, build the library and run the Python test suite under Valgrind to ensure there are no memory leaks.
   - Save the standard error output of Valgrind to `/home/user/project/valgrind_report.txt` using the following command:
     `valgrind --leak-check=full --error-exitcode=1 python3 -m unittest discover -s tests > /home/user/project/valgrind_report.txt 2>&1`

Your final deliverable is a functional, organized project where `make` builds the library, the tests pass, and `valgrind_report.txt` shows 0 bytes definitely lost.