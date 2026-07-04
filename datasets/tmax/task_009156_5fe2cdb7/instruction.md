You are a web developer working on a high-performance backend feature that filters incoming API requests based on Client Version limits. To maximize throughput, the semantic version comparison logic and custom base64-encoded payload parser are written in C as a shared library. A Python test suite uses property-based testing to verify the mathematical correctness of the semantic version logic against Python's standard libraries.

Currently, the C library has a mathematical logic bug in its semantic version comparison, and the `Makefile` is incomplete and fails to build the shared library properly.

Your task:
1. Fix the `Makefile` in `/home/user/app` so that running `make` correctly compiles `semver_check.c` into a shared object library named `libsemver.so`.
2. Find and fix the logic flaw in `/home/user/app/semver_check.c`'s version comparison algorithm. It should strictly implement standard Semantic Versioning precedence (Major.Minor.Patch) where `version1 >= version2`.
3. Run the property-based tests using `pytest /home/user/app/test_semver.py` and redirect standard output to `/home/user/test_result.log` (make sure the tests pass!).

The Python test suite feeds base64-encoded structs (our custom data encoding) to your C library via ctypes and checks the results across thousands of generated test cases. Do not modify the Python test file. 

When you have successfully fixed the C code, compiled the library, and generated a passing test log at `/home/user/test_result.log`, you are done.