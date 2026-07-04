You are a Site Reliability Engineer (SRE) investigating an issue with a custom C utility used to monitor system uptime. 

There is a directory at `/home/user/uptime_monitor` containing:
1. `requests.log`: A log file containing the status of periodic health checks.
2. `monitor.c`: A C program intended to parse this log, calculate the uptime percentage, and print it.
3. `Makefile`: A simple makefile to build the `monitor` executable.

Currently, the utility is failing on three fronts:
1. It fails to build due to a compilation error.
2. It is querying/opening the wrong data source, resulting in no data being processed.
3. The formula used to calculate the uptime percentage is incorrectly implemented, which would result in an inaccurate metric (like 0.00%) even if the data was loaded properly. The correct formula is: `(Total_Requests - Error_Requests) / Total_Requests * 100`.

Your task is to:
1. Fix the build failure in `/home/user/uptime_monitor/monitor.c`.
2. Fix the data source query bug so it correctly reads `/home/user/uptime_monitor/requests.log`.
3. Fix the formula implementation so it calculates the true floating-point percentage of uptime (e.g., if there are 5 total requests and 2 errors, it should be exactly 60.00%).
4. Recompile the program using `make`.
5. Run the fixed `monitor` executable and redirect its standard output to exactly `/home/user/uptime_report.txt`.

Ensure the final report file contains exactly the output of the fixed C program. Do not add any extra text to the file.