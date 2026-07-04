You are an engineer tasked with porting a minimal reverse proxy router to run within an ultra-lightweight Linux container. As part of this effort, you must ensure that the core routing logic, which relies on semantic version (semver) comparisons, is robustly tested. Because the container is minimal, you cannot use external C testing frameworks; you must write a standalone C unit test program and a shell-based integration script.

You have been provided with two files containing the routing logic:
- `/home/user/router.h`
- `/home/user/router.c`

These files implement a function `int cmp_version(const char* v1, const char* v2)` which parses two semantic version strings (e.g., "1.2.3") and returns:
- `1` if `v1` > `v2`
- `-1` if `v1` < `v2`
- `0` if `v1` == `v2`

Your task is to write the test suite:

1. Create a C program at `/home/user/test_router.c` that includes `router.h` and tests the `cmp_version` function. You must test exactly the following four version pairs and assert the correct expected results:
   - "1.0.0" and "1.0.0" (Expected: 0)
   - "2.1.0" and "2.0.9" (Expected: 1)
   - "1.9.0" and "1.10.0" (Expected: -1)
   - "2.0.0" and "1.99.9" (Expected: 1)
   If all tests pass, the program should print `ALL TESTS PASSED` to standard output and exit with code 0. If any test fails, it should exit with a non-zero code.

2. Create a Bash script at `/home/user/build_and_test.sh`. The script must:
   - Compile `router.c` and `test_router.c` into an executable named `/home/user/test_router` using `gcc`.
   - Execute the compiled `/home/user/test_router`.
   - If the tests execute successfully (exit code 0), write the exact string `UNIT: OK` to a new file `/home/user/test_results.log`.
   - If the tests fail, write `UNIT: FAIL` to `/home/user/test_results.log`.
   - Next, to simulate a reverse proxy integration test, the script should write the string `upstream backend { server 127.0.0.1:8080; }` to a file `/home/user/proxy.conf`, and then append `INTEGRATION: OK` to `/home/user/test_results.log`.

Ensure your bash script is executable (`chmod +x`). 
Run your script once to generate the final log file and proxy config so that the test harness can verify your work.