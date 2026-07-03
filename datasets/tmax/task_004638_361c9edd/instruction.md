You are a mobile build engineer maintaining a CI/CD pipeline. Part of the pipeline involves quickly calculating checksums of build artifacts to ensure they aren't corrupted during transfer. For performance, the checksum algorithm (a standard CRC32) is implemented in a compiled C library (`libfastchk.so`), and invoked via a Python wrapper using `ctypes`.

However, the pipeline is currently failing. The Python wrapper `/home/user/checksum_wrapper.py` is buggy. It incorrectly defines the C function signatures and passes arguments improperly, which leads to type mismatch errors, memory corruption, or segmentation faults during FFI (Foreign Function Interface) calls.

Your task is to fix the wrapper and verify the integration:

1. **Debug and Fix FFI:** Edit `/home/user/checksum_wrapper.py` to fix the `ctypes` argument types, return types, and pointer passing. The C function signature in `libfastchk.so` is:
   `int calculate_checksum(const char* input, int length, unsigned int* output);`
   It returns `0` on success and non-zero on failure. The `output` pointer is where the checksum is written.

2. **Write a Unit Test:** Create a Python test script at `/home/user/test_checksum.py` using the standard `unittest` module. It must import `get_checksum` from `checksum_wrapper` and assert that the checksum of the byte string `b"test"` evaluates correctly (you can use Python's built-in `zlib.crc32` to find the expected value). The script must exit with code 0 on success.

3. **Calculate Target Checksum:** Once your wrapper is fixed, use it to calculate the checksum of the exact byte string `b"MOBILE_BUILD_PIPELINE_STABLE"`. Write the resulting integer (as a base-10 string) to `/home/user/result.txt`.

Ensure your test passes and the result file contains only the correct integer. Do not modify the compiled C library.