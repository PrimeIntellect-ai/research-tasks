You are tasked with migrating a legacy Web Application Firewall (WAF) routing component from Python 2 to Python 3. The WAF validates URL parameters and ensures data integrity using an error-correcting checksum (a custom Hamming-based code) appended to route paths. This prevents parameter tampering before requests are forwarded downstream.

The system relies on a high-performance validation function written in Rust, which interfaces with Python via `ctypes`. However, the current migration attempt is broken, the Rust code fails to compile due to ownership and borrow checker errors, and the Python code needs to be updated to Python 3 and optimized to meet strict WAF latency requirements.

Your objectives:

1. **Fix the Rust Extension:**
   Navigate to `/home/user/router_mig/validator/`. The Rust source code in `src/lib.rs` has borrow checker errors. Fix the errors so the code compiles into a shared library (`cdylib`) using `cargo build --release`. The library exposes a `validate_url_checksum` C-FFI function.

2. **Python 2 to Python 3 Migration & Integration:**
   In `/home/user/router_mig/`, you will find `legacy_router.py`. Rename this to `router.py` and update it to Python 3.
   The `router.py` must define a function:
   `def parse_and_validate(url: str) -> dict:`
   This function must:
   - Parse the URL to extract the path and query parameters (using `urllib.parse`).
   - Call the compiled Rust `validate_url_checksum` function via `ctypes` to verify the `data` parameter against the `chk` parameter.
   - Return a dictionary in the exact format: `{"valid": bool, "route": "/the/path", "params": {"data": "...", "chk": "..."}}`. If parsing fails, return `{"valid": False, "route": "", "params": {}}`.

3. **Property-Based Testing:**
   We have provided a stripped, statically compiled reference binary at `/app/ref_router`. This binary takes a URL as a command-line argument and prints the expected JSON output to `stdout`.
   Write a property-based test script at `/home/user/router_mig/test_router.py` using the `hypothesis` library to generate random URL structures. Your test must assert that the output of your `router.py`'s `parse_and_validate(url)` matches the JSON output of `/app/ref_router` for all generated URLs.

4. **Performance Benchmarking:**
   The WAF handles heavy traffic. Your Python 3 + Rust implementation must be highly optimized. We will run an automated benchmark on your `router.py` that processes 10,000 URLs. To pass, your implementation must complete the 10,000 validations in under 0.8 seconds while maintaining 100% accuracy against the reference binary. Ensure your `ctypes` bindings are loaded efficiently (e.g., not re-loading the `.so` file on every function call) and URL parsing overhead is minimized.

Environment details:
- Rust/Cargo and Python 3.10+ are pre-installed.
- You can install any standard python test tools (`hypothesis`, `pytest`) via `pip`.
- Do not modify the reference binary `/app/ref_router`.