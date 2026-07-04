You are an on-call engineer responding to a 3am PagerDuty alert. A critical monitoring cron job is failing. The job runs a Bash script located at `/home/user/monitor/calc_stats.sh` which reads a list of request latencies from `/home/user/monitor/latencies.txt` and calculates the Mean and Standard Deviation. 

Recently, the service moved to a new high-precision timer, and the latencies are now being reported as very large numbers with small fractional differences (e.g., `100000000.001`). Since this change, the `calc_stats.sh` script has started crashing with a fatal math error, failing to output the metrics.

Your task:
1. Diagnose the numerical instability causing the script to crash. You may want to use a debugger or insert debug statements to inspect the memory and variables.
2. Modify `/home/user/monitor/calc_stats.sh` to fix the numerical instability. You must use a numerically stable algorithm (like Welford's online algorithm) to compute the variance and standard deviation in a single pass without precision loss. You must keep Bash as the primary script, though embedded tools like `awk` or `bc` are permitted.
3. Run your fixed script on `/home/user/monitor/latencies.txt`.
4. The script should output the metrics to stdout. Format the output to exactly 3 decimal places.
5. Save the final output of your fixed script to `/home/user/monitor/stats_output.txt`.

The format of `/home/user/monitor/stats_output.txt` must be exactly:
```
Mean: <value>
StdDev: <value>
```

Ensure your fix is robust for similar datasets.