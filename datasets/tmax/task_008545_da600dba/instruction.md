You are a performance engineer analyzing the tail latency of a microservice. You have been provided with a raw log file at `/home/user/perf_logs.csv` containing observed request data with columns `timestamp, endpoint, latency_ms, payload_size`.

Your task is to model the batch processing latency for large payloads on a specific endpoint using a Monte Carlo simulation, and perform a convergence test on your estimates.

Please perform the following steps:
1. Parse `/home/user/perf_logs.csv` and extract the `latency_ms` values for rows where `endpoint` is exactly `/api/v1/process` and `payload_size` is greater than `500`. These are your empirical "large payload" latencies.
2. We want to estimate the 99th percentile (P99) latency of processing a batch of 50 such requests sequentially. The total latency of a batch is the sum of 50 independent samples (drawn with replacement) from your empirical large payload latencies.
3. Write a Python script to perform a Monte Carlo simulation to estimate this P99 batch latency, and test the convergence of your simulation for $N$ iterations (where $N$ is the number of simulated batches). Test for $N \in \{1000, 5000, 10000, 50000\}$.
4. To ensure deterministic results, you must use the following exact procedure for each $N$:
   - Set `numpy.random.seed(42)` immediately before generating the samples for that $N$.
   - Use `numpy.random.choice(empirical_latencies, size=(N, 50), replace=True)` to generate the multi-dimensional array of samples.
   - Sum across the second dimension (size 50) to get an array of $N$ batch latencies.
   - Calculate the 99th percentile of these batch latencies using `numpy.percentile(batch_latencies, 99)`.
5. Save the convergence results to `/home/user/convergence_log.txt`. Each line should correspond to an $N$ value in ascending order, formatted exactly as:
`N=<iterations>, P99=<value>`
where `<value>` is rounded to exactly 2 decimal places (e.g., `N=1000, P99=25345.67`).

Write and execute the Python script to generate this log file.