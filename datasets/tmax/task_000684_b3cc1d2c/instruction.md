You are a platform engineer maintaining a CI/CD pipeline for a data science team. They have a mathematical Python application that relies on a custom, high-performance C library to compute a specific recurrence relation. 

Currently, the CI pipeline is failing. The Python wrapper (`/home/user/math_project/math_wrapper.py`) is unable to find the compiled shared library at runtime. Furthermore, the original author mentioned that even when the library was found, it returned corrupted data or caused segmentation faults because the ABI boundaries (C types vs Python types) were not explicitly defined.

Your task is to fix the integration and create a robust build-and-test pipeline script.

Here is what you need to do:

1. Look in `/home/user/math_project/`. You will find `fastmath.c`, `math_wrapper.py`, and `test_math.py`.
2. Determine how to compile `fastmath.c` into a shared library named `libfastmath.so` in the same directory.
3. Fix `math_wrapper.py` so that:
   - It reliably loads `libfastmath.so` regardless of the current working directory (e.g., by resolving the path relative to the wrapper script, or by relying on properly set environment variables in the pipeline).
   - It correctly defines the FFI boundaries (`argtypes` and `restype`) for the `compute_seq` C function using `ctypes`. Look at the C source code to understand the expected integer sizes and map them to the correct `ctypes`.
4. Create a Bash shell script at `/home/user/math_project/build_and_test.sh`. This script must:
   - Compile the C code into the shared library.
   - Run the Python test suite (`python3 /home/user/math_project/test_math.py`).
   - If the tests pass, use Python to compute the sequence value for `n = 1000` using the wrapper, and append the exact string `PIPELINE_OK: SEQ_1000=<value>` to `/home/user/pipeline_result.log` (where `<value>` is the computed result).

Make sure the bash script has executable permissions. Your final verification will be executing `/home/user/math_project/build_and_test.sh` and checking the contents of `/home/user/pipeline_result.log`.