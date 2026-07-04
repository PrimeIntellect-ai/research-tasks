You are an open-source maintainer reviewing a broken Pull Request. A contributor submitted a PR that refactors a simple math evaluation CLI tool to use a shared library (`libexpr.so`), and they added a Bash-based CI pipeline script to test it. However, the CI pipeline is failing due to compilation, ABI/linking issues, and bugs in the Bash testing logic.

Your environment is located at `/home/user/project`. 
Here is the layout of the project:
- `src/expr.c`: The C source for the shared library.
- `src/cli.c`: The command-line wrapper that links against the shared library.
- `ci/run_pipeline.sh`: The Bash CI script that builds the project and runs the tests.

Your task is to fix the project so that the CI pipeline passes. Specifically, you must:

1. **Fix the Shared Library Build and Linkage (ABI Management):** 
   The CI script (`ci/run_pipeline.sh`) is currently failing to build the shared library correctly. You need to fix the `gcc` commands in the Bash script to properly compile `src/expr.c` into a shared library (`libexpr.so`) using position-independent code. Furthermore, `src/expr.c` contains an ABI issue: the core evaluation function `evaluate_math` is currently hidden or misconfigured, causing a linking/runtime error in the CLI. Fix `src/expr.c` so the symbol is correctly exported and accessible to `cli.c`.

2. **Fix the CI Test Logic (Expression Parsing and Evaluation):**
   The `ci/run_pipeline.sh` script dynamically generates a set of mathematical string expressions (e.g., `"3 + 5 * 2"`). It attempts to run the compiled CLI tool and compare its output with an expected result. However, the Bash logic that calculates the *expected* result is broken. Modify `ci/run_pipeline.sh` so that it correctly evaluates these string expressions in Bash (you may use `bc` or Bash's arithmetic expansion) to get the true expected value.

3. **Pass the Pipeline:**
   When the pipeline successfully builds the library, runs the CLI, and verifies that all CLI outputs match the expected Bash-evaluated results, the script must write the exact string `PIPELINE_SUCCESS` to `/home/user/pipeline_status.txt` and exit with code 0.

Constraints:
- Do not bypass the tests. You must actually fix the build steps, the C ABI issue, and the Bash evaluation logic.
- You must run the tests dynamically inside `ci/run_pipeline.sh`.
- Use `/home/user/project/libexpr.so` and `/home/user/project/expr_cli` for the compiled artifacts.
- You do not have root access. All tools needed (`gcc`, `bc`, `bash`) are already installed.