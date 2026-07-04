You are a Site Reliability Engineer (SRE) investigating an anomaly in a monitoring tool.

We have a simple C program located at `/home/user/latency_monitor.c` that reads server latencies (integers) from a log file and calculates the 99th percentile (P99) latency. 

Recently, we noticed a statistical anomaly: when the monitoring service processes small log batches (e.g., fewer than 1000 entries), the P99 latency reported is sometimes wildly incorrect—either negative or randomly huge. It seems to happen consistently with smaller files.

Your task:
1. Review `/home/user/latency_monitor.c` and identify the logical bug causing these anomalous statistics.
2. Fix the bug and save the corrected code to `/home/user/latency_monitor_fixed.c`. 
3. Create a minimal reproducible example (MRE) input file at `/home/user/mre_input.txt` that contains exactly 10 lines, with the number `50` on each line.
4. Compile your fixed code into an executable named `/home/user/monitor_fixed`. Use standard gcc (`gcc -O0 -o /home/user/monitor_fixed /home/user/latency_monitor_fixed.c`).
5. Run your fixed executable against the MRE file and redirect the standard output to `/home/user/fixed_output.log`.

Ensure all requested files are exactly in the paths specified.