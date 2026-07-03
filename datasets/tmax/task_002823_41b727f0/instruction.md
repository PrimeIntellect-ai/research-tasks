You are a mobile build engineer maintaining a cross-platform CI/CD pipeline. Part of your build process involves passing app manifest strings through a native C library to normalize them. 

Currently, the native module in `/home/user/native_module` is broken. The `Makefile` has a linking error and fails to generate a shared library (`libprocessor.so`). Furthermore, the previous Python integration was plagued by memory leaks because it did not correctly manage pointers returned by the C code.

Your tasks are:

1. **Fix the Makefile**: 
   Navigate to `/home/user/native_module` and fix the `Makefile` so that running `make` successfully compiles `processor.c` into a shared library named `libprocessor.so`.

2. **Build the FFI Wrapper**:
   Write a Python script at `/home/user/process_manifest.py` that utilizes the `ctypes` module to load `/home/user/native_module/libprocessor.so`.

   The C library exposes three functions:
   - `char* process_string(const char* input)`: Implements a state machine to remove consecutive duplicate characters from a string. It allocates and returns memory for the new string.
   - `void free_string(char* ptr)`: Frees the memory allocated by `process_string`.
   - `int get_active_allocations()`: Returns the current number of unfreed memory allocations.

   Your Python script must:
   - Read all strings from `/home/user/inputs.txt` (one per line, stripping the newline character).
   - Pass each string to `process_string` and retrieve the resulting normalized string.
   - Ensure you correctly type the C functions in Python so you do not lose the raw pointer reference. If you use `ctypes.c_char_p` as a return type, Python will cast it to a string immediately and you will permanently lose the pointer needed to free the memory!
   - Explicitly call `free_string` on the returned pointer to prevent memory leaks.
   - Write the normalized strings to `/home/user/outputs.txt`, one per line.
   - After processing all lines, call `get_active_allocations()`. Write the integer returned by this function as the final line in `/home/user/outputs.txt`. If you managed memory correctly, this final line should be `0`.

Run your Python script to generate `/home/user/outputs.txt`.