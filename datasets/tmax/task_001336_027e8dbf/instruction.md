You are helping a developer who is migrating a legacy Python 2 web security backend to Python 3. The system relies on a high-performance C extension to parse custom security tokens from web request headers. The migration is hitting multiple roadblocks, similar to a cascading dependency failure:

1. The legacy C extension (`/home/user/project/c_ext/fast_sec.c`) compiles under Python 3 but causes a segmentation fault when processing large tokens due to a memory safety issue (undefined behavior introduced by a naive migration to Python 3's C API).
2. Anticipating issues with the C extension, the developer started rewriting the parser in Rust (`/home/user/project/rust_ext/src/lib.rs`) using `pyo3`. However, the Rust code currently fails to compile due to ownership and borrow checker errors.
3. The test suite needs a proper fixture setup to validate both extensions against structured JSON data.

Your task is to fix the entire pipeline:

**Step 1: Fix the C Extension**
Examine `/home/user/project/c_ext/fast_sec.c`. It contains a memory safety bug when handling string lengths from Python. Fix the bug so it safely processes strings up to 256 characters without crashing. Build and install it into the current Python environment (you can use `pip install -e .` inside `c_ext`).

**Step 2: Fix the Rust Extension**
Examine `/home/user/project/rust_ext/src/lib.rs`. It attempts to perform the exact same token parsing as the C extension but fails to compile due to a lifetime/borrowing error returning a reference to a local variable. Fix the Rust code so it compiles and correctly returns the owned parsed string. Build and install it (e.g., using `pip install maturin && maturin develop` inside `rust_ext`).

**Step 3: Setup Test Fixtures and Run Tests**
In `/home/user/project/tests/test_parser.py`, write a `pytest` test suite that:
- Reads the structured data from `/home/user/project/data.json`.
- Implements a mock setup: create a mock web `Request` object class that has a `headers` dictionary.
- Transforms the JSON data to populate these mock objects.
- Feeds the `X-Sec-Token` header from each mock request into both `fast_sec.parse_token()` and `rust_sec.parse_token()`.
- Asserts that both extensions return the exact same parsed string.

**Validation:**
Run your `pytest` suite and redirect the standard output to `/home/user/project/test_results.log`. An automated verification script will check this log file to ensure that tests passed successfully and both extensions were exercised.