You are an SRE at a high-traffic company. You are responsible for an internal Rust microservice that analyzes request latencies to compute SLA metrics: specifically the mean latency and its variance over millions of requests.

Recently, the metrics dashboard has been showing impossible values. Specifically, the variance sometimes drops below zero or reports as 0.0, and the mean is systematically under-reporting during high-traffic periods (when logs are largest).

The codebase is located at `/home/user/uptime_stats`.

The service reads a binary file of `f32` latency values (little-endian) and computes the metrics using a multithreaded approach. 

There are three main bugs in the `src/main.rs` implementation:
1. **Concurrency/Logic Bug**: The parallel chunking mechanism drops some data points.
2. **Precision Loss**: Summing millions of `f32` values is resulting in catastrophic precision loss (the sum stalls because the delta is smaller than the float's unit in the last place).
3. **Numerical Instability**: The variance formula being used (`E[X^2] - E[X]^2`) is numerically unstable and causes catastrophic cancellation for floating-point values with small variance.

Your task:
1. Identify and fix the parallel processing logic to process *all* data points.
2. Fix the summation precision loss (e.g., by accumulating in a higher precision type).
3. Fix the numerical instability in the variance calculation (e.g., use a stable two-pass algorithm or Welford's algorithm).
4. Run your fixed Rust program against the provided latency data file located at `/home/user/uptime_stats/data/latencies.bin`.

Once you have the correct metrics, write them to `/home/user/solution.txt` in exactly this format:
```
Mean: <value to 4 decimal places>
Variance: <value to 4 decimal places>
```
*(Example: `Mean: 100.0000`, `Variance: 0.0100`)*

Do not change the input file. You can modify the Rust code however you see fit, as long as it executes concurrently and produces mathematically correct results for the whole dataset.