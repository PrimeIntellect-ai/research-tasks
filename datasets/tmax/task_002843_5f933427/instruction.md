You are a systems programmer debugging an FFI integration between a C library, a Rust wrapper, and a Python test suite. The project is located at `/home/user/project`. 

There are currently three problems preventing the system from working:
1. **Linking Issue**: The Rust wrapper (`/home/user/project/rust_wrapper`) fails to link against the compiled C library (`libc_lib.so`). The C library source is in `/home/user/project/clib`. 
2. **Rust Ownership Bug**: Even if linking is fixed, the Rust code (`/home/user/project/rust_wrapper/src/lib.rs`) has an ownership/borrow checker bug where it returns a pointer to a freed string. 
3. **Missing Python Test**: We need a test script (`/home/user/project/test_ffi.py`) to verify the integration.

**Your objectives:**
1. Compile the C library `/home/user/project/clib/c_lib.c` into a shared library named `libc_lib.so` in the `/home/user/project/clib` directory.
2. Fix the linking issue in the Rust project (hint: check `/home/user/project/rust_wrapper/build.rs`) so it can find and link `libc_lib.so`.
3. Fix the borrow checker / lifetime bug in `/home/user/project/rust_wrapper/src/lib.rs`. The function `get_combined_message` should safely transfer ownership of the created `CString` to C/Python (preventing it from dropping at the end of the function).
4. Build the Rust project (`cargo build --release`). It is configured to produce a `cdylib` named `librust_wrapper.so` in `target/release`.
5. Write the Python test script `/home/user/project/test_ffi.py` using Python 3. The script must:
    * Use `ctypes` to load `/home/user/project/rust_wrapper/target/release/librust_wrapper.so`.
    * Call the `get_combined_message` function, which returns a `c_char_p`.
    * Decode the returned bytes to a UTF-8 string.
    * Using the `unittest.mock` module, set up a mock object that simulates a data fetch returning a list of strings: `["Zebra", "Apple", "Mango"]`.
    * Merge the decoded string from the Rust library into this mock list.
    * Sort the merged list alphabetically.
    * Use Python's `difflib` module to generate a unified diff between the sorted list and an expected list read from `/home/user/project/expected.txt`. (Treat each list element as a line, adding newlines for the diff input).
    * Write the unified diff string to `/home/user/project/diff.txt`.

The expected output file `/home/user/project/expected.txt` contains:
```
Apple
Hello from C and Rust!
Mango
Zebra
```