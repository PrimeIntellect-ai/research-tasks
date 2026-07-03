You are a DevOps engineer investigating an issue with an automated latency metric pipeline. 

A previously running C-based log preprocessor crashed recently, leaving a memory dump at `/home/user/app.core`. The bash scripts that calculate statistics from the logs are also behaving strangely, returning zeros or negative values for variance, which is mathematically impossible.

Here is your task:

1. **Extract Timezone Configuration:**
   The crashed preprocessor had a specific timezone offset in its environment. Analyze the memory dump `/home/user/app.core` and extract the timezone offset string (it will be in the format `CRITICAL_TZ_OFFSET=<offset>`, e.g., `+0200` or `-0500`).

2. **Query Result Debugging (Log Filtering):**
   You have a raw log file at `/home/user/requests.log`. The logs contain UTC timestamps (ISO 8601 format) and latency values (in milliseconds). 
   You need to filter these logs to include **only** the requests that occurred on the local calendar date of `2023-10-25` according to the timezone offset you extracted in Step 1.

3. **Diagnose and Fix Numerical Instability:**
   There is a script at `/home/user/calc_variance.sh` that takes a list of latency values (one per line) from standard input and calculates the population variance. It currently uses a naive `awk` implementation (`Variance = (Sum of Squares / N) - (Mean ^ 2)`).
   Because the latencies are large base numbers (e.g., around $10^8$ ms) with very small fluctuations, standard double-precision floating-point arithmetic in `awk` suffers from catastrophic cancellation, causing the script to output `0` or negative numbers.
   Fix `/home/user/calc_variance.sh` to use a numerically stable algorithm (like Welford's algorithm or a mean-centered two-pass approach) to calculate the population variance. The output must be rounded to exactly 4 decimal places.

4. **Calculate Final Metric:**
   Run your fixed `/home/user/calc_variance.sh` using the filtered latencies from Step 2 as input. Save the single output value to `/home/user/solution.txt`.

5. **Construct a Regression Test:**
   Write a regression test script at `/home/user/regression.sh`. This script must:
   - Feed the values `100000000.1`, `100000000.2`, and `100000000.3` (newline-separated) into `/home/user/calc_variance.sh`.
   - Capture the output.
   - If the output is exactly `0.0067`, exit with code 0.
   - If the output is anything else, exit with code 1.

Ensure all scripts are executable.