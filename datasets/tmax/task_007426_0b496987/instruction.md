You are an operations engineer triaging an incident for a quantitative analytics team. An automated nightly job, which calculates the volume-weighted average yield of a portfolio, is failing and producing incorrect results. 

The application is located in `/home/user/analytics/`. 
You can run the job using `python /home/user/analytics/run_job.py`. Currently, it either crashes with a `ConvergenceError`, or returns mathematically impossible metrics.

Through preliminary investigation, the team has identified three distinct issues in `/home/user/analytics/engine.py` and `/home/user/analytics/run_job.py` that you need to fix:

1. **Query Result Debugging:** The SQLite database query fetching trades is joining with a status table but is returning duplicate trades because it doesn't filter by the current active status, artificially inflating the portfolio size. Modify the query to only include trades where the `status` is exactly `'SETTLED'`.
2. **Floating-point Precision Repair:** The calculation for the `total_portfolio_value` iteratively adds many very small floating-point values to a very large float, resulting in precision loss (truncation). Fix this by using a numerically stable summation method from Python's standard library.
3. **Convergence Failure Repair:** The `calculate_yield` function uses the Newton-Raphson method to find the yield rate, but the stopping criteria uses an exact zero equality check (`if diff == 0.0:`). Due to floating point math, it oscillates and hits the maximum iteration limit, causing a convergence failure. Change the stopping criteria to check if the absolute difference is less than `1e-7`.

Fix the code in `/home/user/analytics/engine.py`. Once fixed, run the job using `python /home/user/analytics/run_job.py`. It should successfully complete and automatically write the final calculated portfolio yield to `/home/user/analytics/result.txt`.

Ensure your final answer leaves the exact computed numerical value inside `/home/user/analytics/result.txt`.