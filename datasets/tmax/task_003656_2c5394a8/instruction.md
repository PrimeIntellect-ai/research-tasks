I am in the process of migrating a legacy Python C-extension from Python 2 to Python 3. The workspace is located at `/home/user/migration`. 

Right now, I am facing two major problems:
1. The build system is broken. The `CMakeLists.txt` is failing at configuration/link time because it's still hardcoded to look for the Python 2 shared libraries, but we need it to compile for Python 3. Fix the `CMakeLists.txt` so it successfully generates the build files and links the `string_ops` module against Python 3.
2. The C code in `extension.c` has been partially updated to the Python 3 API (e.g., using `PyModuleDef`), but testing reveals it has a memory leak that was introduced during the migration. Our long-running workers eventually crash out of memory. 

Your tasks:
1. Update `CMakeLists.txt` to find and link Python 3 correctly.
2. Build the extension (e.g., using `cmake .` and `make`).
3. Run the included `test.py` script and use a memory debugger like `valgrind` to profile the memory issue.
4. Modify `extension.c` to fix the memory leak. Ensure that all dynamically allocated memory in the C extension is properly freed before returning the result to Python.
5. Rebuild the C extension.
6. Once fixed, run the following exact command to generate a verification log:
   `valgrind --leak-check=full python3 test.py > /home/user/migration/success.log 2>&1`

The automated test will inspect `/home/user/migration/success.log` to verify that the program outputs the correctly processed string and that Valgrind reports exactly `0 bytes` definitely lost.