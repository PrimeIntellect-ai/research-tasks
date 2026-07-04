You are an open-source maintainer reviewing a Pull Request for a mathematical constraint satisfaction tool. The contributor has provided three files in `/home/user/pr_review/`:

1. `solver.py`: A Python script that solves the Subset Sum problem. It includes a mock API request validator and a strict local rate limiter (maximum of 2 requests per second).
2. `build.sh`: A configuration script meant to set up environment flags for cross-compilation conditional builds.
3. `e2e_test.sh`: An end-to-end orchestration script that tests the solver.

The PR is currently failing the CI tests. Your task is to fix the PR by addressing the following issues:

1. **Conditional Build Bug:** The `build.sh` script currently hardcodes the architecture configuration to `x86`. Modify `build.sh` so that it uses the `TARGET_ARCH` environment variable if it is set. If `TARGET_ARCH` is not set, it should default to `x86`. The script should write `CONFIG_ARCH=<arch>` to `config.env`.
2. **Rate Limiting / Orchestration Bug:** The `e2e_test.sh` script executes 5 test cases against `solver.py` in rapid succession. Because of the strict 2 req/sec rate limit in `solver.py`, tests 3, 4, and 5 fail with a `429 Rate Limit Exceeded` error. Modify `e2e_test.sh` to orchestrate the tests correctly by adding appropriate delays (e.g., using `sleep`) so that all tests pass without triggering the rate limit. 
3. **Execution:** Once the scripts are fixed, run `bash /home/user/pr_review/build.sh` (with `TARGET_ARCH=arm64` set in your environment), then run `bash /home/user/pr_review/e2e_test.sh`. 
4. **Verification Output:** Save the standard output of the successful `e2e_test.sh` run to `/home/user/test_results.log`.

Do not modify `solver.py`. You only need to fix `build.sh` and `e2e_test.sh`, and generate the final log file.