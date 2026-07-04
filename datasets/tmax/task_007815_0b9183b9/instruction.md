You are a developer tasked with migrating a legacy Python 2 web security tool to Python 3. 

The tool validates custom security tokens used to authenticate requests in an internal microservice. It uses a custom state machine to parse the tokens and relies on a compiled C shared library to compute a checksum for tamper verification.

Currently, the legacy code resides in `/home/user/legacy/`.
It contains:
- `tokenhash.c`: The source code for the hashing library.
- `libtokenhash.so`: The compiled shared library.
- `validator.py`: The Python 2 code containing the state machine parser and `ctypes` wrapper.

Your task is to:
1. Copy `validator.py` to `/home/user/validator.py` and upgrade it to be fully compatible with Python 3.
2. Fix the ABI management in the `ctypes` wrapper. In Python 2, passing strings directly to C functions expecting `char *` worked seamlessly. In Python 3, you must correctly define `argtypes` and `restype` for the C function `uint32_t compute_hash(const char* data, int length)` and ensure Python 3 strings/bytes are passed correctly.
3. Fix the state machine parser (`parse_token` method). The parser reads characters one-by-one to transition through states (`START`, `READ_DATA`, `READ_CHECKSUM`). The Python 3 distinction between `bytes` and `str` breaks the current byte-iteration logic. Ensure the parser accepts a Python 3 `str` token, encodes it to utf-8 internally if necessary, and correctly extracts the `data` and `checksum`. The token format is `SEC<data>#<checksum_in_hex>`.
4. Write a unit test suite using `pytest` in `/home/user/test_validator.py` that imports your updated `validator.py`. The test suite must include at least the following test functions:
   - `test_valid_token()`: Tests a correctly formatted token with a valid checksum (e.g., `SECadmin123#00000000` - you will need to find a real valid checksum).
   - `test_invalid_format()`: Tests a token that breaks the state machine (e.g., missing the `SEC` prefix or `#` delimiter) and asserts it raises a `ValueError`.
   - `test_invalid_checksum()`: Tests a correctly formatted token where the computed checksum does not match the provided checksum, asserting it returns `False`.
5. Run your test suite and save the verbose output to a log file by running: `python3 -m pytest /home/user/test_validator.py -v > /home/user/test_output.txt`

The test output file `/home/user/test_output.txt` must show that all tests passed successfully. Do not modify the C code or recompile the shared library.