You are helping migrate a legacy Python 2 API component to Python 3. To improve performance and security, the team has decided to extract the core numerical algorithm used for API signature generation into a Rust library, which will then be called from Python 3 using `ctypes`.

The legacy Python 2 algorithm for the signature generation is:
```python
def compute_signature(token_id, salt):
    # token_id and salt are 64-bit unsigned integers
    # Constant is a 64-bit prime
    return ((token_id ^ salt) * 11400714819323198485) % (2**64)
```

Please complete the following steps:

1. Create a new Rust library project at `/home/user/rust_validator`.
2. Implement the `compute_signature` logic in Rust. It must accurately reflect the legacy logic using 64-bit unsigned integers and handle overflows appropriately (wrapping behavior). Expose this function to C so it can be called externally (name the exposed function `compute_signature`).
3. Configure the `Cargo.toml` to build a C-compatible dynamic library (`cdylib`). Build the project in release mode.
4. Write a Python 3 wrapper file at `/home/user/py3_wrapper.py`. This file must define a function `compute_signature(token_id: int, salt: int) -> int` that uses the `ctypes` module to load `/home/user/rust_validator/target/release/librust_validator.so` and call the Rust function. Ensure you configure the `argtypes` and `restype` appropriately for 64-bit unsigned integers (`ctypes.c_uint64`).
5. Write a property-based test script at `/home/user/test_validator.py` using `pytest` and `hypothesis`. Create a test `test_signature_equivalence` that generates `token_id` and `salt` as integers between 0 and `2**64 - 1`. The test must assert that your Python 3 wrapper's output exactly matches the expected output from the legacy mathematical logic.
6. Run `pytest /home/user/test_validator.py > /home/user/test_results.log`.

Do not run as root. Ensure all files are placed exactly at the specified paths.