You are tasked with fixing a malfunctioning data processing pipeline for a long-running Python asyncio service. 

Currently, the service processes sensor data from an SQLite database, applies mathematical transformations, and writes the output to a JSON file. However, several critical issues are preventing it from working correctly:

1. **Database Recovery**: The primary database `/home/user/sensor_data.db` was corrupted during a power failure. A WAL file exists, but standard queries fail. You must recover the data into a new valid SQLite database named `/home/user/recovered_data.db`.
2. **Environment Misconfiguration**: The service relies on a shared library for some fast path operations located at `/home/user/libs/libfastmath.so`. The service crashes on startup because it cannot find this library. Fix the environment configuration so the Python service can load it.
3. **Memory Leak**: The service `/home/user/service.py` uses `asyncio` to process records concurrently. It has a severe memory leak related to task cancellation and reference management (the "goroutine leak" equivalent in Python asyncio). Specifically, tasks are stored in a global state to prevent premature garbage collection, but they are never cleaned up after completion. Identify and fix this leak in `service.py`.
4. **Numerical Instability**: The data transformation calculates the variance of sliding windows of float values in `/home/user/math_utils.py`. The current implementation calculates variance using the naive formula: `E[X^2] - (E[X])^2`. For the sensor data (which contains very large baseline numbers with microscopic fluctuations), this causes catastrophic cancellation, resulting in negative or zero variances. Fix `math_utils.py` to use a numerically stable algorithm (like Welford's or `statistics.variance`).
5. **Regression Test Construction**: Create a regression test file at `/home/user/test_regression.py` using standard `unittest` that imports `calc_variance` from `math_utils` and proves it correctly handles the input `[100000000.0, 100000000.00001, 100000000.00002]` without returning exactly `0.0` or throwing an error.

**Instructions:**
- Recover the database to `/home/user/recovered_data.db`.
- Fix the environment, `service.py` (memory leak), and `math_utils.py` (numerical instability).
- Run the fixed service to process all records: `python /home/user/service.py --db /home/user/recovered_data.db --output /home/user/processed_output.json`.
- Write the regression test to `/home/user/test_regression.py`.
- Write a final summary log to `/home/user/fix_summary.log` containing exactly three lines:
  - Line 1: The number of rows recovered in `recovered_data.db`.
  - Line 2: The exact variance value calculated for the list `[100000000.0, 100000000.00001, 100000000.00002]` using your fixed `calc_variance` function.
  - Line 3: The `id` of the last record written to `processed_output.json`.