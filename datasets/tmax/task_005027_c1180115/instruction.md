You are tasked with building a Python orchestration script to fix, compile, and benchmark a broken Rust project. The project is located at `/home/user/rust_processor` and currently fails to compile due to a syntax and logic error.

You must write a Python script at `/home/user/fix_and_bench.py` that performs the following steps in order:

1. **Semantic Version Resolution:**
   Read `/home/user/patches/versions.json`. Find the highest semantic version available in the `"versions"` list that satisfies the constraint `>= 1.1.0, < 2.0.0`.

2. **Checksum Verification:**
   Using the resolved version (e.g., `1.x.x`), locate its corresponding patch file at `/home/user/patches/fix_<version>.patch`. 
   Compute the SHA256 checksum of this patch file and verify it matches the hash provided for that version in `/home/user/patches/checksums.txt`. 

3. **Patch Application:**
   Programmatically apply the verified patch file to the `/home/user/rust_processor` project. You may use Python's `subprocess` to call `patch -p1 < ...` or implement it directly. This patch will fix the Rust compilation errors.

4. **Mock Server Setup:**
   The Rust application, once compiled, expects to fetch data from an API. Your Python script must spawn a background mock HTTP server on `127.0.0.1:8080`. 
   When the Rust app makes a `GET /data` request to this server, the mock must return a 200 OK status with the exact JSON body: `{"status": "success", "payload": 42}`.

5. **Compilation and Benchmarking:**
   - Compile the patched Rust project using `cargo build --release` (executed from within `/home/user/rust_processor`).
   - Run the compiled binary (`/home/user/rust_processor/target/release/rust_processor`) 5 times.
   - Measure the execution time of each run.
   - Calculate the average execution time across the 5 runs in milliseconds.

6. **Reporting:**
   Write the results to a JSON file at `/home/user/report.json` with the following exact keys:
   - `"resolved_version"`: (string) The semantic version you resolved in step 1.
   - `"patch_checksum"`: (string) The SHA256 checksum of the applied patch file.
   - `"average_time_ms"`: (float) The average execution time of the Rust binary in milliseconds.
   - `"mock_hit"`: (boolean) `true` if your mock server successfully received requests.

Ensure your Python script is robust, well-documented, and executable (`python3 /home/user/fix_and_bench.py`). The script must complete all steps without user intervention.