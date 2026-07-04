You are a DevOps engineer tasked with resolving a critical failure in our daily telemetry anomaly detection pipeline. 

Every night, a script runs to pull sensor latency logs from our SQLite database, calculates the variance of the latencies, and uses an iterative optimization algorithm to calibrate our alerting threshold. However, today the script (`/home/user/anomaly_detector.py`) is failing with exceptions and convergence errors due to some edge-case data that entered the logs.

Here are the specific problems you need to identify and fix in `/home/user/anomaly_detector.py`:

1. **Query Result Debugging:** The query fetching data from `/home/user/telemetry.db` is pulling in bad records. Some latency values are recorded as `NULL` or negative numbers due to sensor reboots. You must modify the SQL query or the fetch logic to exclusively process records where the `latency` is a positive number (greater than 0) and the `status` is exactly `'OK'`.
2. **Floating-point Precision Repair:** The variance calculation in the script uses the naive formula `(sum(x^2) - (sum(x)^2)/N) / N`. Because today's valid latencies are very large numbers with tiny differences (e.g., `1000000.001`, `1000000.002`), this formula suffers from catastrophic cancellation, resulting in a negative or highly inaccurate variance. Replace this with a numerically stable method (like Welford's algorithm, or by using Python's built-in `statistics.variance` / `statistics.pvariance`).
3. **Convergence Failure Repair:** The `calibrate_threshold` function uses a simple iterative method to find a threshold. Because of the precision loss and a missing learning rate decay or safety bound, it is currently stuck in an infinite loop or raising a "Failed to converge" error. Fix the convergence loop so that it safely breaks when the delta is smaller than `1e-7`, and ensure it doesn't crash if variance is somehow exactly zero.

**Your Tasks:**
1. Analyze and edit `/home/user/anomaly_detector.py` to fix all three issues.
2. Run the fixed script. It is designed to print a final calibrated threshold (a float).
3. Save the precise printed float value to a file at `/home/user/final_threshold.txt`.

Ensure your fixes are robust. Do not hardcode the expected threshold; the script must calculate it correctly based on the database contents.