You are tasked with fixing a failing Rust project located at `/home/user/rust_project`. The build currently fails due to several distinct issues that a previous developer left behind.

Here is what you need to do:
1. **Recover the Secret:** The test suite expects a `.env` file in the project root (`/home/user/rust_project/.env`) containing a valid `SECRET_TOKEN=...` key-value pair. The token was accidentally committed in the past, but the developer overwrote it with "REDACTED" in a later commit. Use git history forensics to find the original secret token and restore the `.env` file.
2. **Fix the Race Condition:** Running `cargo test` often results in failures in the `storage` module. This is because multiple tests run concurrently and write to a hardcoded temporary file path, causing a race condition. Modify `src/storage.rs` (or its tests) so that the tests can run concurrently in `cargo test` without interfering with each other. (Using unique file paths or thread-local storage is recommended).
3. **Fix the Floating-Point Instability:** A test in the `analytics` module is failing because of numerical instability. The function `sum_large_metrics` in `src/analytics.rs` accumulates a large array of `f32` values into an `f32` sum, losing precision along the way. Fix the implementation of this function so that it internally uses `f64` for the accumulation to preserve precision, then casts the final sum back to `f32`.

Once you have fixed the code and the tests pass via `cargo test`, create a file at `/home/user/success.txt`. 
The file must contain exactly two lines:
Line 1: The recovered secret token value (just the value itself, e.g., `my_secret_123`).
Line 2: The exact string `TESTS_PASSED`.

Do not change the test assertions themselves; only fix the underlying implementations or the file paths used by the tests so they pass successfully.