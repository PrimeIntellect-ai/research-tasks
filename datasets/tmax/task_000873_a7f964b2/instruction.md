You are tasked with bisecting and fixing a numerical regression in a data processing pipeline.

The repository is located at `/home/user/pipeline_repo`. It contains a script `process_data.py` that queries a local SQLite database (`/home/user/sensor_data.db`), performs an aggregation using a custom C-extension (`_fast_agg`), and prints a single floating-point result to standard output. 

Recently, a regression was introduced that causes severe numerical instability (yielding wildly incorrect results or `NaN`s) on our production datasets. The regression happened somewhere within the last 200 commits.

We have provided a stripped, compiled binary at `/app/oracle_bin`. This binary serves as the ground-truth oracle: it correctly reads `/home/user/sensor_data.db` and prints the accurate, numerically stable result to standard output.

Your objectives:
1. **Bisect the Regression**: Use `git bisect` to find the exact commit that introduced the numerical instability. Be aware that some commits in the repository history suffer from C-extension linker errors (missing math library flags), which you will need to interpret and bypass or fix during bisection. Write the full 40-character commit hash of the first bad commit to `/home/user/bad_commit.txt`.
2. **Fix the Bug**: Fix the codebase at the current `HEAD` so that the numerical instability is resolved. The bug involves how variance or exponential sums are aggregated. You must fix the algorithm.
3. **Match the Oracle**: The output of `python /home/user/pipeline_repo/process_data.py` must match the output of `/app/oracle_bin`.

You can test the oracle by simply running `/app/oracle_bin`. Do not modify the database or the oracle. Ensure your final fixed code is committed or left in the working tree at `/home/user/pipeline_repo/process_data.py`.