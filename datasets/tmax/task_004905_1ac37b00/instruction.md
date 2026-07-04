You are a systems programmer tasked with fixing an FFI (Foreign Function Interface) and ABI compatibility issue in a Python application. 

You have been given the source code for two versions of a C library, `libdata`, located in `/home/user/src/v1/` and `/home/user/src/v2/`.

Your tasks are:
1. **Build the Shared Libraries:**
   Compile the C files in both directories into shared libraries.
   - The version 1 library must be compiled and linked to `/home/user/lib/libdata.so.1`.
   - The version 2 library must be compiled and linked to `/home/user/lib/libdata.so.2`.
   Create the `/home/user/lib/` directory if it does not exist.

2. **Write the Python FFI Wrapper:**
   Write a Python script at `/home/user/app.py` that accepts exactly two command-line arguments:
   `python3 /home/user/app.py <library_path> <input_string>`

   The script must use `ctypes` to load the shared library specified by `<library_path>` and dynamically handle ABI differences based on the library's semantic version:
   - Call the C function `const char* get_version()` exposed by the library to retrieve its semantic version.
   - Perform a semantic version comparison. 
   - **If the major version is 1 (e.g., < 2.0.0):**
     The library exposes `void encode_data(const char* input, char* output)`. 
     You must pass the `<input_string>` encoded as standard UTF-8 bytes. The output buffer will be populated with a UTF-8 string.
   - **If the major version is 2 (e.g., >= 2.0.0):**
     The library had an ABI break and now exposes `void encode_data_wide(const wchar_t* input, wchar_t* output)`.
     You must pass the `<input_string>` as wide characters (`wchar_t`). The output buffer will be populated with wide characters.
   
   The Python script must print the final encoded string to standard output, followed by a newline.

3. **Execute and Log:**
   Run your script against both libraries with the input string `"TestString123"` and redirect the standard output to the following files:
   - Run with `libdata.so.1` -> save output to `/home/user/result_v1.txt`
   - Run with `libdata.so.2` -> save output to `/home/user/result_v2.txt`

Ensure your Python script cleanly handles the memory allocation for the output buffers (a buffer of 256 characters is sufficient for this task).