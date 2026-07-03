You are a Linux systems engineer tasked with hardening a custom filesystem monitoring configuration. A previous engineer designed a monitoring system that occasionally writes logs to the wrong directory because it fails to inherit the correct environment variables when executed by automated schedulers (like cron). 

Your task is to implement the monitoring tool in C, write a robust shell wrapper that guarantees the correct environment, create a health-check script, and set up a persistent environment profile.

Perform the following steps exactly as specified:

1. **Write the C Monitoring Tool (`/home/user/src/monitor.c`)**
   Write a C program that performs a simple filesystem directory check.
   - It must read two environment variables: `DATA_DIR` and `MONITOR_OUTPUT_PATH`.
   - If `MONITOR_OUTPUT_PATH` is not set, it must default to `/home/user/wrong_logs/fallback.log`.
   - If `DATA_DIR` is not set, print an error to standard error and exit with code 1.
   - Use the `stat()` system call to verify that the directory specified by `DATA_DIR` exists and is a directory.
   - If the directory exists, append the exact string `STATUS: OK - <value_of_DATA_DIR>\n` to the file specified by `MONITOR_OUTPUT_PATH`.
   - If the directory does not exist or is inaccessible, append `STATUS: ERROR - <value_of_DATA_DIR>\n` to the file and exit with code 2.
   - Compile this C program to the executable path `/home/user/bin/monitor`.

2. **Write a Robust Wrapper Script (`/home/user/bin/run_monitor.sh`)**
   Automated job runners often run with a very minimal environment. Write a bash script to safely wrap the C binary.
   - The script must use robust error handling (fail on non-zero exit codes, fail on unbound variables).
   - It must ensure the directory `/home/user/logs` exists, creating it if necessary.
   - It must explicitly export `DATA_DIR="/home/user/data"`.
   - It must explicitly export `MONITOR_OUTPUT_PATH="/home/user/logs/monitor_status.log"`.
   - It must execute the `/home/user/bin/monitor` binary.
   - Ensure the script is executable.

3. **Write a Health Check Script (`/home/user/bin/health_check.sh`)**
   Write a bash script that acts as an independent health check.
   - The script must read `/home/user/logs/monitor_status.log`.
   - If the last line of the log file starts with `STATUS: OK`, the script should print "HEALTHY" to standard out and exit with code 0.
   - Otherwise, it should print "UNHEALTHY" and exit with code 1.
   - Ensure the script is executable.

4. **Environment Profile Setup**
   To ensure interactive users are aware of the system state, append the following line exactly to `/home/user/.bash_profile`:
   `export MONITOR_CONFIGURED=true`

*Note: You must create `/home/user/src`, `/home/user/bin`, `/home/user/wrong_logs`, and `/home/user/data` directories if they do not exist before executing your code.*