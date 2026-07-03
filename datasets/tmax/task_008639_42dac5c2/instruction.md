I am a developer debugging a failing build process for our analytics pipeline, and I need your help to fix it. The build occasionally fails, and I suspect it is a combination of a misconfigured environment and a bug in our mathematical calculations.

Here is the setup:
The project is located in `/home/user/workspace`. 
When I run `make stats` in that directory, it is supposed to read metrics files and compute the variance of the data chunks. However, it fails with errors. 

Your tasks are to:
1. **Fix the Environment Misconfiguration**: The `Makefile` currently sets an invalid environment variable that causes the script to fail to find the data directory. Modify the `Makefile` to set `METRICS_DIR` to the correct absolute path: `/home/user/workspace/data`.
2. **Fix the Formula / Intermittent Bug**: The Python script `src/compute_stats.py` calculates sample variance. Occasionally, a data chunk only contains a single value, which causes the script to crash with a `ZeroDivisionError` because the formula divides by `count - 1`. Modify `src/compute_stats.py` so that if the length of the data is 1 or less, the `calculate_variance(data)` function returns `0.0`.
3. **Write a Regression Test**: Create a regression test file at `/home/user/workspace/test_regression.py`. It should import `calculate_variance` from `src.compute_stats`, pass a single-element list (e.g., `[42.0]`) to it, and assert that the returned value is exactly `0.0`. 
4. **Generate Verification Logs**: 
   - Run your regression test and save the output to `/home/user/workspace/test_output.log`. (e.g., `python3 test_regression.py > /home/user/workspace/test_output.log 2>&1`)
   - Run the fixed build process using `make stats` and save the successful output to `/home/user/workspace/build_success.log`.