You are a release manager preparing a deployment pipeline. Part of the application relies on a highly optimized Rust library accessed via Python using Foreign Function Interface (FFI). 

Unfortunately, the previous engineer left the integration incomplete:
1. The Rust library has a compile-time lifetime/borrow checker error preventing it from being built.
2. The Python test suite is currently using a mock object in its `pytest` fixture instead of loading the compiled shared library via `ctypes`.

Your tasks are:
1. Fix the compile-time borrow checker error in `/home/user/release_prep/rust_ffi/src/lib.rs`. Ensure the function safely passes ownership of the generated string to C (e.g., via `into_raw`).
2. Build the Rust library in release mode (it should produce a `cdylib` `.so` file in the `target/release` directory).
3. Modify the test fixture in `/home/user/release_prep/test_release.py`. Remove the mock. Load the compiled Rust shared object (`librust_ffi.so`) using `ctypes.CDLL`. You must correctly configure the `.argtypes` and `.restype` for the `generate_release_tag` function (it takes a C string and returns a C string).
4. Run `pytest /home/user/release_prep/test_release.py` and redirect the standard output to `/home/user/release_prep/test.log`.

Ensure the tests pass and the real Rust binary is being invoked by the Python code.