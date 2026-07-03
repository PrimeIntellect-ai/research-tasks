You are acting as an integration developer testing a high-performance API security scanner. The scanner consists of a Python frontend and a Rust backend (using PyO3) designed to fuzz web APIs. The test suite passes locally on the original developer's machine but fails in our CI environment. Furthermore, the performance is currently abysmal during certain integration tests.

You have been provided with the following files and directories:
1. `/home/user/api_scanner/` - The source code directory containing:
   - `Cargo.toml` and `src/lib.rs` (The Rust backend FFI module `fast_fuzzer`)
   - `scanner.py` (The Python wrapper)
   - `requirements.txt`
   - `tests/test_integration.py`
2. `/app/fuzz_session.mp4` - A screen recording from the CI runner showing the exact sequence of 5 critical security payloads (in hex format) that trigger the performance degradation.

Your goals:

1. **Video Analysis**: Use `ffmpeg` and any standard CLI tools (or write a Python script) to extract the 5 critical hex payloads from the video `/app/fuzz_session.mp4`. The payloads appear on screen one by one prefixed with "CRASH_PAYLOAD: ". Save these payloads, one per line, in `/home/user/api_scanner/extracted_payloads.txt`.

2. **Fix the Rust Backend**: The Rust code in `src/lib.rs` currently uses an inefficient cloning mechanism and has a borrow checker / lifetime bug preventing it from safely borrowing string slices from Python. Modify `src/lib.rs` to fix the borrow checker errors so it compiles, and ensure it correctly references the memory without unnecessary allocation. Build the Python extension in release mode.

3. **Fix the Python CI Bug**: The Python script `scanner.py` fails in CI due to a strict import ordering issue. The Rust extension `fast_fuzzer` currently panics or deadlocks if it is imported before the Python `ssl` and `requests` modules are fully initialized in the CI's monkey-patched environment. Refactor `scanner.py` so the module imports are correctly ordered.

4. **Benchmark Script**: Create a benchmark script at `/home/user/api_scanner/benchmark.py` that reads the 5 payloads from `extracted_payloads.txt`, initializes the `fast_fuzzer` API, and processes the payloads 10,000 times sequentially. The script must output the total time taken in seconds to `stdout` in the format: `Throughput: <float> seconds`.

The automated verifier will compile your code and run its own measurement tool to check if the Rust/Python FFI integration meets the strict performance threshold.