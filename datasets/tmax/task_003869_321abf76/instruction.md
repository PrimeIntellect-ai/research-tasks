You are a build engineer managing artifacts for a multi-language project. We have a Go application located in `/home/user/project` that implements a numerical algorithm to solve a subset sum constraint satisfaction problem.

Currently, the build pipeline is failing because of a circular import issue between the `solver` and `utils` packages in the Go code. 

Your tasks are:
1. Analyze the Go source code in `/home/user/project` and refactor it to resolve the circular import. You must ensure the numerical constraint satisfaction algorithm remains functionally correct.
2. Build the compiled Go binary and output it exactly to `/home/user/project/app`.
3. We have an end-to-end Python orchestration script located at `/home/user/project/e2e_test.py` that automatically tests the compiled binary against several constraints. Run this Python script.
4. Redirect the standard output of the `e2e_test.py` script to a log file at `/home/user/project/test_results.log`.

Do not change the inputs tested by the Python script. Ensure your final log file correctly captures the output of the end-to-end test suite.