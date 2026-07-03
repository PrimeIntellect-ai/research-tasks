You are a performance engineer tasked with debugging a metric aggregation pipeline.

Our system generates 50 daily log files containing profiling metrics. To speed up the processing, a previous engineer wrote a Bash script `/home/user/perf_profiling/summarize.sh` that iterates over these log files and uses a compiled helper binary `/home/user/perf_profiling/metric_filter` to quickly sum up the execution times found in the logs.

However, we are seeing intermittent, impossible negative values in our reports. Specifically, one of the log files produces a negative total execution time. We suspect the `metric_filter` binary has a bug (likely a signed integer overflow on x86/x64 architectures when the total execution time exceeds a certain threshold), but the source code for the binary has been lost.

Your task:
1. Navigate to `/home/user/perf_profiling/` and run the existing pipeline to identify the failure.
2. Analyze the output and reverse engineer the behavior of the `metric_filter` binary to confirm the cause of the failure.
3. Write a new Bash script `/home/user/perf_profiling/fixed_summarize.sh` that implements a robust fix. Since the binary source code is lost, your script should completely replace the binary's aggregation logic using standard shell utilities (like `awk`, `bc`, or pure bash). It must output to `results.txt` in the exact same format as the original script, but with correct (positive) totals for all files.
4. Document your specific finding in a file at `/home/user/perf_profiling/overflow_report.txt`. The file must contain exactly one line with the name of the failing log file and its true correct total, separated by a single space.
   Format: `<filename> <correct_total>`
   Example: `log_15.txt 2800000000`

Ensure your new script `fixed_summarize.sh` is executable.