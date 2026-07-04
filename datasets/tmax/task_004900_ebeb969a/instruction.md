You are a software engineer tasked with debugging a regression in a time-series sensor data processing pipeline. 

The repository is located at `/home/user/sensor_project`.
Recently, the CI pipeline has been failing intermittently on the `main` branch when running `pytest tests/test_pipeline.py`. The failure is an `AssertionError` related to final aggregated values not matching expected tolerances, suggesting a precision loss was introduced somewhere in the processing logic. 

Your tasks are:
1. **Reproduce the Intermittent Failure:** The test in `tests/test_pipeline.py` uses randomized sensor data. You will need to write a deterministic wrapper or use pytest tools to reliably trigger the failure.
2. **Git Bisection:** The tag `v1.0` is known to be perfectly stable and passes all tests. The current `main` branch `HEAD` is broken. Use `git bisect` to find the exact commit that introduced the regression. 
3. **Record Findings:** Once you find the bad commit, write its full, exact SHA-1 hash to `/home/user/bad_commit.txt`.
4. **Minimal Reproducible Example (MRE):** The bug is located in `src/math_utils.py` inside the `apply_calibration` function. Create a minimal script at `/home/user/mre.py` that imports `apply_calibration`, passes the float `100.0` to it, and uses an `assert` statement to validate that the function returns exactly `100.023` without any precision loss (truncation or rounding). 
5. **Fix the Bug:** Modify `src/math_utils.py` to fix the precision loss so that `pytest tests/test_pipeline.py` passes reliably.

Ensure that `/home/user/bad_commit.txt` contains *only* the bad commit hash, and `/home/user/mre.py` runs successfully (exit code 0) after you fix the bug.