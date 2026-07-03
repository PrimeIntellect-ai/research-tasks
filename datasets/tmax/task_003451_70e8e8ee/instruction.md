You are an engineer investigating a suspected memory leak in a long-running service. 

You have been provided with a historical log file of memory snapshots taken from the service's subsystems. The file is located at `/home/user/service_mem.log`.

The log file has the following expected format for valid lines:
`[TIMESTAMP] PID COMPONENT_NAME MEMORY_IN_MB`

However, the logging system was unstable, so the log file contains several corrupted lines (e.g., stack traces, partial writes, or binary garbage). You must safely ignore these malformed lines.

Your task:
1. Parse `/home/user/service_mem.log` using standard shell tools.
2. Filter out corrupted or malformed lines. A valid line strictly has four space-separated columns: a timestamp in brackets, an integer PID, a string component name, and an integer memory value.
3. For each valid PID, calculate the total memory leaked. The "leaked memory" is defined as the difference between the *last* recorded memory value and the *first* recorded memory value for that PID chronologically.
4. Identify the PID responsible for the largest memory leak (the highest positive difference).
5. Write your findings to exactly `/home/user/leak_report.txt` in the following format:
`PID: <LEAKING_PID>, LEAK_MB: <DELTA>`

For example, if PID 9999 started at 100 MB and its last log entry was 500 MB, and this was the highest increase, the file should contain exactly:
`PID: 9999, LEAK_MB: 400`