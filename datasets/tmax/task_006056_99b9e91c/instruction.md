You are a platform engineer maintaining a CI/CD pipeline for a legacy internal tool. A recent commit broke the test pipeline for a C-based custom data structure (a priority queue) used for job scheduling.

Your task is to fix the build configuration and the Bash-based integration testing script, then generate the final test report.

Navigate to `/home/user/ci_cd_test/`. Inside, you will find:
1. C source files (`main.c`, `pqueue.c`, `pqueue.h`) which implement the priority queue.
2. A broken `Makefile`.
3. A broken Bash test runner `run_tests.sh`.

Perform the following:
1. **Fix the Makefile**: The `Makefile` has standard syntax errors and compilation bugs preventing it from building the target executable `pqueue_app`. Fix it so that running `make` successfully compiles the application.
2. **Fix the Bash Test Runner**: The `run_tests.sh` script is supposed to use a Bash associative array to map test inputs to their expected outputs. However, it fails with syntax errors or logic errors when iterating through the custom test cases. Correct the Bash script so it correctly iterates over the associative array, runs `./pqueue_app` with the given inputs, and verifies the output.
3. **Generate the Test Report**: Once both are fixed, run `./run_tests.sh` and redirect its standard output to `/home/user/ci_cd_test/test_report.txt`.

The final `test_report.txt` must contain the exact passing output from the test script, which should look like:
```
Test 'push 5, push 10, pop' - PASS
Test 'push 1, pop, pop' - PASS
...
```

Make sure that `make` succeeds and `test_report.txt` is created with all tests passing.