You have just inherited a data processing codebase located at `/home/user/stats`. The project contains a Go package used to detect statistical anomalies (outliers) in arrays of floating-point numbers using the Z-score method.

However, the previous developer left the codebase in a broken state:
1. The test suite fails to run due to an environment misconfiguration.
2. Once the environment is fixed, the tests still fail because there is a logical flaw in the Z-score formula implementation.

Your tasks are:
1. Identify and fix the environment misconfiguration so that `make test` successfully executes the test suite without panicking. You must modify the `Makefile` to permanently fix the environment issue for the `test` target.
2. Investigate the mathematical anomaly in `stats.go`. Use intermediate validation and delta debugging if necessary to find the root cause of why the anomaly detection returns incorrect results. 
3. Correct the Z-score formula implementation in `/home/user/stats/stats.go`. 
4. Verify your fix by running `make test`.
5. Once the tests pass, create a file at `/home/user/success.txt` containing the exact string `ALL TESTS PASSED`.

Constraints:
- Do not modify `stats_test.go`. You must make the existing assertions pass.
- Do not change the function signatures.
- Standard libraries only.