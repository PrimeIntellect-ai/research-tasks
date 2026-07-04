You are helping a team migrate an old legacy system. We have a numerical tool in `/home/user/migrator` that computes a moving average. It consists of a C implementation, a Go command-line wrapper using CGO, and an integration test written in Python 2. 

The team wants to modernize this component and fix a known critical bug.

Your tasks:
1. **Fix the C Memory Safety Bug**: The function in `moving_average.c` currently returns a pointer to a local stack array, which causes undefined behavior and memory corruption. Fix `moving_average.c` to properly allocate the result array on the heap using `malloc`. Ensure you return the allocated pointer. 
2. **Migrate the Integration Test**: The script `integration.py` is currently written in Python 2. Migrate it to Python 3. You must fix all Python 2 specific syntax (like `print` statements) so that it runs without errors under `python3`.
3. **Write a Go Unit Test**: Create a file `/home/user/migrator/main_test.go`. Write a Go test function `TestComputeMA` that tests the `computeMA` function inside `main.go`. Assert that `computeMA([]float32{1.0, 2.0, 3.0, 4.0}, 2)` returns `[]float32{1.5, 2.5, 3.5}`.
4. **Build and Orchestrate**: Create a bash script `/home/user/migrator/build_and_test.sh` that does the following in order:
   - Compiles the Go application to an executable named `ma_cli`.
   - Runs the Go unit tests (`go test`).
   - Runs the newly migrated Python 3 integration test (`python3 integration.py`).
   - If all the above steps succeed (exit code 0), write the exact string `ALL TESTS PASSED` to `/home/user/migrator/success.log`.

Make sure all commands in your bash script are executable and fail-fast (e.g., using `set -e`). Do not change the function signatures in `moving_average.h`.