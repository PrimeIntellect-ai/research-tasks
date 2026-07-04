You are a Site Reliability Engineer (SRE) investigating an issue with your team's custom uptime monitoring daemon. The daemon aggregates health-check logs from multiple containers to calculate the average system latency, but it has recently started crashing during its hourly run, leaving your monitoring dashboards blank.

The source code for the aggregator is located at `/home/user/aggregator/aggregate.cpp`. It reads a log file located at `/home/user/logs/metrics.log`.

The log file format is expected to be:
`timestamp|container_id|status|latency_ms`

However, some containers occasionally experience timeouts, resulting in log entries that look slightly different and trigger a format parsing edge-case bug in the C++ code, causing the program to terminate abruptly.

Your task:
1. Diagnose the bug in `/home/user/aggregator/aggregate.cpp` by inspecting the logs in `/home/user/logs/metrics.log` and analyzing the code's string parsing logic.
2. Fix the C++ code so that it safely ignores the `latency_ms` value for any log entry where the `status` is not `OK` or the latency field is missing, without crashing. 
3. Recompile the program using `g++ -O2 -o aggregate aggregate.cpp`.
4. Run the compiled program and redirect its standard output to `/home/user/final_metrics.txt`.

The program, once fixed, should successfully parse the entire log file and print out the correct average latency (using integer division) to the output file.