You are an integration developer responsible for optimizing a text processing API. Part of the API's encoding logic is being migrated to Rust to improve performance. However, the CI/CD pipeline is currently failing because the Rust component has an ownership/borrow-checker-related memory safety bug, and the Python integration tests have not been set up.

Your task is to fix the Rust library, implement a Python benchmarking script to compare it against a pure Python implementation, and set up a basic CI script to automate the process.

Here are the requirements:

1. **Fix the Rust Engine:**
   There is a Rust project located at `/home/user/engine`. It provides a Run-Length Encoding (RLE) function exposed as a C-compatible shared library. 
   - Currently, `src/lib.rs` has a severe memory/ownership bug where it returns a dangling pointer because the `CString` is dropped at the end of the function.
   - Fix `src/lib.rs` so that it safely transfers ownership of the string to the caller (e.g., using `into_raw()`). 
   - Ensure you can build it successfully using `cargo build --release` inside `/home/user/engine`.

2. **Python Integration and Benchmark:**
   Write a Python script at `/home/user/api_test.py` that does the following:
   - Reads the UTF-8 text from `/home/user/data.txt`.
   - Implements a pure Python version of Run-Length Encoding (RLE). The RLE should count consecutive identical characters (e.g., "aaabbc" becomes "a3b2c1").
   - Loads the compiled Rust shared library (`/home/user/engine/target/release/libengine.so`) using `ctypes`. Note: The Rust function signature is `extern "C" fn encode_rle(input: *const c_char) -> *mut c_char`. Make sure to configure `argtypes` and `restype` properly.
   - Asserts that both the Python implementation and the Rust implementation produce the exact same encoded string for the data in `/home/user/data.txt`.
   - Benchmarks both implementations by running them each 1,000 times on the data from `data.txt`.
   - Outputs the results to `/home/user/benchmark_report.json` in exactly this format:
     ```json
     {
       "match": true,
       "rust_time": 0.0015,
       "python_time": 0.045
     }
     ```
     (Where the time values are the float durations in seconds for the 1000 iterations).

3. **CI/CD Script:**
   Create a bash script at `/home/user/ci_run.sh` that automates this. The script must:
   - Compile the Rust code in release mode.
   - Run the `api_test.py` script.
   - Exit with code 0 if successful, or code 1 if any step fails.
   Make sure to make the script executable (`chmod +x`).

The starting file `/home/user/data.txt` contains a mix of repeated UTF-8 characters (e.g., emojis and standard letters). Do not modify `/home/user/data.txt`.