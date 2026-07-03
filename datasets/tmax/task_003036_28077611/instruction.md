You are a systems programmer debugging a C library linking and ABI issue in a Linux environment.

In the directory `/home/user/app/`, there is a pre-compiled dynamically linked binary named `server_bin` and a shared library named `libauth.so`. 

When you try to run `./server_bin`, it fails to start or crashes because `libauth.so` depends on an external function that is missing from the system libraries. Specifically, the original `libcrypto.so` it was built against is not present, leaving an unresolved symbol issue.

Your task is to:
1. Identify the exact name of the missing missing C function required by `libauth.so`.
2. Write a minimal mock implementation of this missing function in C. Create this file at `/home/user/app/mock_crypto.c`. The function should accept a single `const char*` argument and simply return the integer `1` (indicating success).
3. Compile `mock_crypto.c` into a shared library named `libmock_crypto.so` in the `/home/user/app/` directory.
4. Write a Bash script at `/home/user/app/test_fixture.sh` that runs `./server_bin` and successfully injects your mock library (e.g., using `LD_PRELOAD` or `LD_LIBRARY_PATH` combined with linker flags, depending on how you build it) so that the unresolved symbol is satisfied.
5. The `test_fixture.sh` script must capture the standard output of the `server_bin` execution and save it exactly to `/home/user/app/test_result.log`.

Ensure that:
- `/home/user/app/test_fixture.sh` has executable permissions.
- You do not modify `server_bin` or `libauth.so`.
- Your bash script correctly isolates the test environment.