You are a log analyst investigating performance patterns on a distributed cluster. You have been given a massive log file of interleaved telemetry data in a "long" format, and you need to process it efficiently into a "wide" format for a monitoring dashboard.

The raw log file is located at `/home/user/raw_metrics.log`.
Each line in this file contains three space-separated fields:
`[UNIX_TIMESTAMP] [METRIC_CODE] [VALUE]`

The `METRIC_CODE` is an integer representing:
* `1` - CPU Usage (percentage)
* `2` - Memory Usage (megabytes)
* `3` - Disk IOPS

Your task is to write a highly efficient C program at `/home/user/process_logs.c` that does the following:
1. Reads this space-separated data from standard input (`stdin`).
2. Aligns (floors) every `UNIX_TIMESTAMP` to the nearest 60-second bucket (e.g., timestamps `1700000015` and `1700000059` both become `1700000000`).
3. Groups the records by this 60-second bucket.
4. Aggregates the data by calculating the **maximum** value observed for each of the three metrics within each bucket.
5. Reshapes the data into a wide CSV format.
6. Outputs the results to standard output (`stdout`) in the following format:
   `BUCKET_TIMESTAMP,MAX_CPU,MAX_MEM,MAX_DISK`
   * Values should be printed as floats with exactly two decimal places (e.g., `45.50`).
   * If a specific metric has no readings in a given bucket, its maximum should be reported as `0.00`.

After writing the C program, compile it to `/home/user/process_logs`.
Process the entire `/home/user/raw_metrics.log` through your program, sort the resulting lines chronologically by the bucket timestamp (ascending), and save the final output to `/home/user/aggregated_metrics.csv`.

Example expected output line:
`1700000060,89.50,4096.00,0.00`