You are a Site Reliability Engineer (SRE). You've been provided with a C program, `/home/user/uptime_analyzer.c`, that parses a system event log and calculates the total uptime in seconds. 

The system log is located at `/home/user/system.log`. The log format is expected to be:
`YYYY-MM-DD HH:MM:SS STATUS`
Where `STATUS` is strictly either `UP` or `DOWN`.

However, the log generation system occasionally outputs corrupted lines. The parser must completely ignore any line that does not strictly match the expected format with a valid date and a status of either `UP` or `DOWN`. Such malformed lines should have no effect on the uptime calculation.

Additionally, the C program has a subtle time-parsing bug that causes it to yield incorrect or non-deterministic results when compiled and run. 

Your task:
1. Identify and fix the bugs in `/home/user/uptime_analyzer.c`.
2. Ensure the code correctly ignores corrupted or unrecognized input lines.
3. Compile the fixed C program.
4. Run it against `/home/user/system.log`.
5. Write only the final numerical total uptime (in seconds) to a file named `/home/user/uptime_result.txt`.

Ensure your C program is robust and follows standard POSIX time parsing practices.