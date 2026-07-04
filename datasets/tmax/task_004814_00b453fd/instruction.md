You are acting as a capacity planner analyzing system resource usage. You need to set up a small tracking utility in C, configure a specific directory structure with symlinks, ensure timestamps are recorded in a specific timezone, and implement a basic log rotation script.

Please complete the following steps:

1. **Directory and Link Setup:**
   - Create the directory `/home/user/capacity/logs` and `/home/user/capacity/logs/archive`.
   - Create a symbolic link at `/home/user/capacity/active_logs` that points to `/home/user/capacity/logs`.

2. **C Tracker Program:**
   - Write a C program in `/home/user/capacity/tracker.c`.
   - The program must take exactly one command-line argument: the path to an output log file.
   - The program must read the 1-minute load average from `/proc/loadavg` (the first space-separated value).
   - The program must append a single line to the specified log file in the exact following format:
     `[YYYY-MM-DD HH:MM:SS TZ] LOAD: <load_value>`
     *(Example: `[2023-10-24 10:15:30 HST] LOAD: 0.15`)*
   - Ensure the timezone abbreviation (`TZ`) is obtained using the `%Z` format specifier in `strftime`.
   - Compile the program to an executable named `/home/user/capacity/tracker` using `gcc`.

3. **Timezone Configuration and Execution:**
   - Run your compiled `/home/user/capacity/tracker` executable exactly once. 
   - Pass `/home/user/capacity/active_logs/resource.log` as the output file argument.
   - IMPORTANT: The program must be executed such that the local timezone is temporarily evaluated as `Pacific/Honolulu` (which uses the `HST` abbreviation year-round). Do not change the system-wide timezone (you do not have root access); use environment variables to enforce this for the execution.

4. **Log Rotation Script:**
   - Write a bash script at `/home/user/capacity/rotate.sh`.
   - The script must move `/home/user/capacity/logs/resource.log` to `/home/user/capacity/logs/archive/resource_rotated.log`.
   - Make the script executable, but **do not run it**. We will run it during verification.