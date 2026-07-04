You are a DevOps engineer responsible for maintaining a real-time log analysis pipeline. The pipeline consists of three inter-dependent services communicating via named pipes:

1. **`log_gen`**: Generates high-precision response time metrics (large integers in nanoseconds) and writes them to `/tmp/raw_logs`.
2. **`processor`**: Reads the response times from `/tmp/raw_logs`, computes a running mean and running sum of squared differences, and writes the results to `/tmp/stats`.
3. **`log_alert`**: Reads from `/tmp/stats` and triggers alert logs to `/home/user/alerts.log` if anomalies are found.

Currently, the pipeline is failing. The `processor` service relies on a Bash/Awk script located at `/home/user/processor.sh`. If you check the supervisor logs (e.g., `/var/log/supervisor/processor-stderr.log`), you will see that `log_alert` is rejecting the data. 

Your investigation indicates two mathematical flaws in `/home/user/processor.sh`:
- **Boundary Condition Error:** The script fails or divides by zero on the very first log line.
- **Convergence / Precision Failure (Catastrophic Cancellation):** The script computes the variance using the naive formula (Sum of Squares - Square of Sums / N). Because the response times are very large (e.g., ~1,000,000,000), floating-point limits are exceeded, resulting in negative variance or NaNs. 

We have provided a compiled reference binary at `/app/oracle_processor` that performs the exact required mathematical calculations correctly using **Welford's Online Algorithm**. 

Your tasks:
1. **Fix the Math:** Rewrite the `/home/user/processor.sh` script using `awk` or `bc` to process standard input line-by-line. Implement Welford's online algorithm to avoid catastrophic cancellation. For every input line (a single integer `x`), it must output exactly:
   `n mean sum_squared_diff`
   where `n` is the 1-indexed line count, `mean` is the running mean, and `sum_squared_diff` is the running sum of squared differences from the mean (not the variance). Format the `mean` and `sum_squared_diff` to exactly 4 decimal places. The output must be bit-exact to what `/app/oracle_processor` produces for any sequence of inputs.
2. **Re-integrate the Pipeline:** Once `/home/user/processor.sh` is fixed, ensure the pipeline processes data continuously. Update any broken configurations in `/etc/supervisor/conf.d/pipeline.conf` if necessary, restart the supervisor services using `supervisorctl`, and verify that `/home/user/alerts.log` begins populating with alert evaluations.

Ensure your script is robust and executable. The automated verifier will strictly test your `/home/user/processor.sh` script against the oracle using thousands of random large integer sequences.