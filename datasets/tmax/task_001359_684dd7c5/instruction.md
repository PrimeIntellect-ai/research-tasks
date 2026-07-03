You are an open-source maintainer for a high-performance C library called `fast-telemetry` located in `/home/user/fast-telemetry`. A contributor submitted a pull request that adds a fast-path delta encoding for telemetry metrics using inline assembly, a custom circular buffer, and a structured configuration parser. However, the PR is broken and fails the continuous integration tests.

Your task is to check out the PR branch, fix the broken code, ensure the test fixture is properly mocked, build the project, and run the tests.

Here are the specific steps you must complete:

1. **Checkout the PR branch:** The repository is currently on `master`. Switch to the branch `pr-104-fast-delta`.

2. **Fix Assembly-Level Delta Calculation (`src/delta_calc.c`):**
   The function `void compute_deltas(const int32_t* curr, const int32_t* prev, int32_t* out, size_t len)` uses inline x86_64 assembly. The contributor made a mistake, and it is currently adding the values instead of subtracting them. Fix the inline assembly so it correctly computes `out[i] = curr[i] - prev[i]`. Do not remove the inline assembly; fix it.

3. **Complete the Custom Data Structure (`src/buffer.c`):**
   The PR introduces a `CircularDeltaBuffer`. The `push_buffer` and `pop_buffer` functions are incomplete. Implement them so they correctly handle a fixed-size ring buffer of `int32_t` values. The structure is defined in `include/telemetry.h`.
   - `bool push_buffer(CircularDeltaBuffer* cb, int32_t val)`: Adds to the buffer. Returns `false` if full.
   - `bool pop_buffer(CircularDeltaBuffer* cb, int32_t* val)`: Removes from the buffer. Returns `false` if empty.

4. **Implement Structured Data Parsing (`src/config.c`):**
   Implement `int parse_config(const char* filepath, Config* cfg)`. The configuration file consists of key-value pairs in the format `KEY=VALUE\n`. Ignore empty lines. Return `0` on success, `-1` on failure. You must extract the `MAX_BUFFER_SIZE` key (integer) and store it in `cfg->max_buffer_size`.

5. **Fix the Test Fixture (`tests/test_main.c`):**
   The test suite currently tries to write telemetry data to a real file `/etc/telemetry.log`, which fails due to permissions. Modify `tests/test_main.c` to use a mock sink. The library exposes a function pointer `void (*write_sink)(const char* data)`. Create a mock function in the test file that appends the data to a global string buffer `char mock_output[1024]`, and assign this mock function to `write_sink` before the tests run.

6. **Build and Test:**
   - Run `make` in `/home/user/fast-telemetry`.
   - Run `make test` and pipe the output to `/home/user/test_results.log`.

For the task to be considered complete, `/home/user/test_results.log` must exist and contain the phrase "ALL TESTS PASSED".