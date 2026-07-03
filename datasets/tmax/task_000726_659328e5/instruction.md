You are helping a developer reorganize a messy workspace and set up cross-language testing for a custom C++ data structure.

The directory `/home/user/messy_workspace` currently contains a jumble of C++ files for a `StringHistory` class (a custom data structure that remembers the last `N` added strings). 

Your task is to reorganize the project, create a C-compatible FFI wrapper, compile it into a shared library, and write a Python integration test.

Follow these exact steps:

1. **Reorganize the files:**
   Create a new directory structure at `/home/user/project/` with the following subdirectories:
   - `src/`
   - `include/`
   - `lib/`
   - `tests/`
   Move `string_history.hpp` from the messy workspace into `include/`.
   Move `string_history.cpp` from the messy workspace into `src/`.

2. **Create the C-FFI Wrapper:**
   Write a new file `/home/user/project/src/c_api.cpp` that provides an `extern "C"` interface to the `StringHistory` class. It must export the following exact functions:
   - `void* History_create(int capacity);` (returns a pointer to a newly allocated StringHistory)
   - `void History_destroy(void* obj);` (deletes the StringHistory object)
   - `void History_add(void* obj, const char* str);` (calls the `add` method)
   - `const char* History_get(void* obj, int index);` (calls the `get` method)

3. **Compile the Shared Library:**
   Compile `string_history.cpp` and `c_api.cpp` into a shared library named `libhistory.so` located in `/home/user/project/lib/`. Make sure to compile with `-fPIC -shared` and include the `include/` directory in the header search path.

4. **Write the Python Integration Test:**
   Create a Python script at `/home/user/project/tests/test_ffi.py`.
   This script must use the `ctypes` module to load `/home/user/project/lib/libhistory.so` and test the data structure.
   The script must:
   - Create a history object with a capacity of 2.
   - Add the strings "apple", "banana", and "cherry" in that order.
   - Assert that getting index 0 returns "cherry" (as it's the most recent).
   - Assert that getting index 1 returns "banana".
   - Assert that getting index 2 returns `None` or a null pointer (since capacity is 2).
   - Clean up the history object.
   - If all assertions pass, it must write the exact string `ALL TESTS PASSED` to `/home/user/project/test_results.log`.

Execute your Python test script to ensure the log file is generated successfully.