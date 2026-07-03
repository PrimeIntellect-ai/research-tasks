I am an open-source maintainer reviewing a pull request for our data pipeline tool. A contributor submitted a PR that offloads our legacy JSON schema migration to a fast Rust library using FFI (`ctypes`). However, the PR is broken: the Rust code doesn't even compile due to an ownership/borrow checker error, and the Python test script is missing.

Your task is to fix the PR, build the shared library, and write the missing Python integration test to verify the pipeline.

Here is the current state of the system:
1. The Rust project is located at `/home/user/rust_parser`. It builds a `cdylib` named `librust_parser.so`.
2. Inside `/home/user/rust_parser/src/lib.rs`, there is an FFI function called `migrate_schema(input: *const c_char) -> *mut c_char` and a cleanup function `free_string(ptr: *mut c_char)`. The `migrate_schema` function attempts to parse an old JSON format and return a new schema, but it currently fails the borrow checker because it returns a pointer to a dropped `CString`.
3. There is a legacy data file at `/home/user/legacy_input.txt` containing base64-encoded data.

Please do the following:
1. Fix the borrow checker/lifetime error in `/home/user/rust_parser/src/lib.rs`. Ensure that it safely returns a pointer that Python can read without causing a use-after-free or dangling pointer.
2. Compile the Rust library in release mode (the library will be output to `/home/user/rust_parser/target/release/librust_parser.so`).
3. Write a Python script at `/home/user/test_migration.py` that:
   - Reads the base64 string from `/home/user/legacy_input.txt`.
   - Base64-decodes the string into bytes.
   - Loads the compiled Rust library using `ctypes`.
   - Sets the proper `argtypes` and `restype` for both `migrate_schema` and `free_string`.
   - Passes the decoded bytes to the `migrate_schema` function.
   - Reads the returned C-string pointer, decodes it to a Python string, and immediately passes the pointer to `free_string` to avoid memory leaks.
   - Parses the returned string as JSON and writes it to `/home/user/migrated_output.json` using `json.dump` with `indent=2`.

Ensure you run your Python script so that `/home/user/migrated_output.json` is generated.