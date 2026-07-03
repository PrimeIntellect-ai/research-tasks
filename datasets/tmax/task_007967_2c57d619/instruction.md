You are helping a developer migrate a legacy reverse proxy configuration system from Python 2 to Python 3. The old system used a C extension to parse a custom binary routing protocol, but for the Python 3 migration, we are rewriting the parser in Rust and exposing it via a C ABI. You need to implement this Rust parser and test it via Python 3 `ctypes`.

Your task:
1. Create a new Rust library project at `/home/user/rust_lib`.
2. Configure it to compile as a C dynamic library (`cdylib`) with the library name `proxy_abi`.
3. In `src/lib.rs`, design a custom data structure and parser to handle the following binary proxy route format:
   - `route_type`: 1 byte (must be `0x01` for a valid reverse proxy route).
   - `path_len`: 2 bytes (Big Endian unsigned integer) representing the length of the path string.
   - `path`: UTF-8 string of `path_len` bytes.
   - `target_len`: 2 bytes (Big Endian unsigned integer) representing the length of the target URL.
   - `target`: UTF-8 string of `target_len` bytes.
4. Expose a C-ABI compatible function exactly with this signature (equivalent in C):
   `int32_t extract_target(const uint8_t* input, size_t len, char* output, size_t out_len);`
   - The function should parse the `input` buffer.
   - If `route_type` is exactly `0x01` and the `path` exactly matches `"/api/v3"`, it should copy the `target` string into the `output` buffer (null-terminated) and return the length of the target string.
   - If the input is invalid, `route_type` is wrong, or `path` doesn't match, return `-1`.
   - Prevent buffer overflows (do not write more than `out_len` bytes).
5. Build the Rust library.
6. Write a Python 3 test script at `/home/user/test_proxy.py` that:
   - Uses the `ctypes` module to load the compiled Rust shared library (`/home/user/rust_lib/target/debug/libproxy_abi.so`).
   - Constructs a binary payload matching the format above, where `path` is `"/api/v3"` and `target` is `"http://backend_service:9090"`.
   - Calls the `extract_target` function.
   - Writes the extracted target string returned in the output buffer to `/home/user/result.log` (just the string, no newlines).
7. Execute `/home/user/test_proxy.py` to generate the log file.