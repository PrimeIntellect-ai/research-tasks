You are a Site Reliability Engineer (SRE) investigating an issue with a custom uptime monitoring tool written in C. The tool reads a log of service state changes and calculates the overall uptime percentage. However, the tool is currently malfunctioning.

There is a log file located at `/home/user/uptime_logs.txt`. Each line contains a Unix timestamp and a status code (`1` for UP, `0` for DOWN). The last line of the file contains the word `END`.

The source code for the monitoring tool is located at `/home/user/monitor.c`. It has a couple of severe bugs:
1. It never finishes executing (it hangs indefinitely).
2. When the hanging issue is bypassed, the calculated uptime and total time values are incorrect due to a subtle flaw in how the numerical values are handled (the timestamps are large epoch times, but the durations between them are very small).

Your task is to:
1. Identify and fix the loop termination bug that causes the program to hang.
2. Identify and fix the numerical instability/precision loss issue so that the durations are calculated with high accuracy.
3. Compile your fixed version.
4. Run the fixed program and redirect its standard output to `/home/user/fixed_output.txt`.

The format of `/home/user/fixed_output.txt` must exactly match the output format of the original program:
```
Total Time: <value>
Uptime: <value>
Percentage: <value>
```

Constraints:
- Do not change the overall logic of how uptime is calculated.
- The standard C library should be sufficient.