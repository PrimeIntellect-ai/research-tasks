You are an IT support technician responding to an urgent ticket regarding a failed reporting pipeline.

**Ticket Description:**
"Our overnight metric processing job crashed. The script `/home/user/calculate_cooling.awk` parses `/home/user/system_metrics.log` but is failing with a mathematical error (likely a divide-by-zero or similar anomaly) because of an edge case in the temperature readings.

Additionally, a race condition in the logger caused some exact duplicate lines to be written to the log file. 

Please resolve this ticket by performing the following steps using standard Linux terminal tools:
1. Identify the race condition artifacts in `/home/user/system_metrics.log` and deduplicate the file. You must strictly preserve the original chronological order of the first occurrence of each line.
2. Fix the formula in `/home/user/calculate_cooling.awk`. The script calculates a 'cooling factor' using the formula `FAN_RPM / (CPU_TEMP - 20)`. Modify the awk script so that if `CPU_TEMP` (the second column) is exactly 20 or less, the resulting cooling factor should simply be output as `0`.
3. Run your fixed awk script on the cleanly deduplicated log file data.
4. Save the final output to `/home/user/fixed_report.txt`.

**Log Format:**
`TIMESTAMP CPU_TEMP FAN_RPM`