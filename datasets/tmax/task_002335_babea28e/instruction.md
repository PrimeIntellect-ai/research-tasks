You are an integration developer working on a C++ Web Security module that authenticates requests using an external Web Application Firewall (WAF) mock library. 

Currently, the project is in a broken state at `/home/user/workspace/auth_module`. 

You have four objectives to complete this task successfully:

1. **Fix the Build System (Linker Error):**
   The project uses CMake (`/home/user/workspace/auth_module/CMakeLists.txt`). When you try to build it, it fails to link against `libmock_waf.so`. The pre-compiled shared library is located in `/home/user/opt/mock_libs/`. Modify the `CMakeLists.txt` so that the `auth_test` executable correctly finds and links this library at link time AND runtime (using RPATH configuration so it doesn't require setting `LD_LIBRARY_PATH` manually).

2. **Memory Debugging:**
   The integration test `/home/user/workspace/auth_module/auth_test.cpp` contains a memory leak in the `process_token()` function when handling malformed JWT tokens. Find the leak and fix it. 

3. **Constraint Satisfaction & Mock Setup:**
   In `auth_test.cpp`, implement the empty function `generate_attack_payload()`. This function must return a `std::string` that satisfies the following constraints required by the WAF API:
   - Exactly 16 characters long.
   - Starts with the string `"admin"`.
   - The sum of the ASCII values of the remaining 11 characters must be exactly 1000.
   - Only contains printable ASCII characters.

4. **CI/CD Pipeline Setup:**
   Create a bash script at `/home/user/workspace/auth_module/ci_run.sh`. This script should:
   - Make a fresh `build` directory.
   - Run `cmake ..` with `-DCMAKE_CXX_FLAGS="-fsanitize=address -g"` to enable AddressSanitizer.
   - Compile the project (`make`).
   - Run the compiled `./auth_test` executable.
   - Redirect the standard output and standard error of `./auth_test` to `/home/user/workspace/ci_result.log`.
   - Exit with a code of `0` if everything succeeds, or non-zero if the build or test fails.

Ensure all files are saved and `ci_run.sh` is executable. 
Your final deliverable is running `ci_run.sh` successfully, resulting in the creation of a clean `/home/user/workspace/ci_result.log` containing the text `"All tests passed!"` without any ASan error reports.