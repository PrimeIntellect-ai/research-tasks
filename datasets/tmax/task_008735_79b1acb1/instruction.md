You are an IT support technician. We've received an escalated ticket (Ticket #8821) from the data science team. 

They are using a local Rust-based utility called `stat_calc` located at `/home/user/ticket_8821/stat_calc`. They are reporting two major issues:

1. **Environment Issue:** They use a script `/home/user/ticket_8821/stat_calc/run_tests.sh` to run their test suite, but it's immediately failing with a configuration error. The environment variable `STAT_CONFIG_PATH` seems to be misconfigured in the script. It should point to the existing config file inside the project directory.
2. **Floating-Point Precision Bug:** Once the tests run, you'll see a failing test regarding variance calculations. The function `calculate_variance` in `src/lib.rs` uses the naive "sum of squares" method with `f32` arrays. For datasets with a very large mean but tiny variance (e.g., `[100000.0, 100000.1, 100000.2]`), catastrophic cancellation occurs, resulting in 0.0 or even negative variance. 

Your tasks:
1. Fix `run_tests.sh` so the environment is correctly configured and the tests actually execute.
2. Read and comprehend `src/lib.rs`. Fix the `calculate_variance` function to be numerically stable. You can use internal `f64` accumulation, a two-pass algorithm, or Welford's algorithm. The function signature `pub fn calculate_variance(data: &[f32]) -> f32` must remain the same.
3. Construct a regression test. Create a new file `/home/user/ticket_8821/stat_calc/tests/regression_test.rs` containing a standard Rust integration test. This test must call `calculate_variance` with the array `[100000.0, 100000.1, 100000.2]` and assert that the result is approximately `0.006666` (use a tolerance / epsilon of `0.0001`).
4. Ensure `bash run_tests.sh` passes successfully.
5. Create a file at `/home/user/ticket_8821/resolution.txt` containing only the string `RESOLVED`.

You have full access to standard Linux utilities and the Rust toolchain (cargo, rustc).