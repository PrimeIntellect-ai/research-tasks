You are a performance engineer profiling a complex microservices architecture. You have collected a raw execution trace in a CSV file located at `/home/user/perf_trace.csv`.

The file contains an edge-list representation of the service call graph, with the following columns:
`caller_id,callee_id,exec_time_ns`

The execution times (`exec_time_ns`) are extremely large baseline numbers with very small fractional variations (e.g., `9000000000.123`). 

Your task is to identify the primary bottleneck caller and analyze its latency variance using standard Linux command-line tools (e.g., `awk`, `sort`, `join`, etc.). 

Perform the following steps:
1. Parse the call graph and find the node with the highest out-degree (the `caller_id` that calls the highest number of distinct `callee_id`s).
2. For this specific bottleneck caller, calculate the **population variance** of its `exec_time_ns`.
3. **Critical:** Due to the large magnitude of the execution times and the limits of double-precision floating-point numbers in standard tools like `awk`, a naive variance formula ($E[X^2] - E[X]^2$) will suffer from catastrophic cancellation and yield 0 or negative numbers. You must implement a numerically stable algorithm (such as a two-pass method or Welford's algorithm) to compute the variance correctly.
4. Save your final result to `/home/user/bottleneck_analysis.txt` in the following comma-separated format:
   `caller_id,out_degree,variance`
   
Format the variance to exactly 4 decimal places.

For example, if the top caller is `ServiceX` with 12 outgoing calls and a variance of `0.0520`, the file should contain exactly:
`ServiceX,12,0.0520`