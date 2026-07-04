You are a Site Reliability Engineer investigating a recurring outage in a custom uptime monitoring service. 

The service runs a Bash script `/home/user/uptime-monitor.sh` which queries a local SQLite database (`/home/user/monitor.db`) for pending endpoint URLs and passes them to a compiled C helper binary (`/home/user/check_status`) to perform network checks.

Recently, the service has been crashing abruptly. The SQLite database was left in a dirty state with an active Write-Ahead Log (WAL) file (`/home/user/monitor.db-wal`), and the monitoring script is failing to complete its run.

Your task is to debug the system, recover the data, and patch the monitoring script to prevent future crashes. 

Complete the following objectives:

1. **Root Cause Diagnosis**: The `check_status` binary is crashing due to a specific URL in the database. Use interactive debugging tools (`gdb`) or memory/logging analysis to determine exactly which URL is causing the segmentation fault. 
   Write the exact string of the crashing URL to a new file at `/home/user/crash_cause.txt`.

2. **Database Recovery**: The database has uncommitted transactions stuck in the WAL file due to the crash. Recover the database so it is fully consistent. Extract all URLs (both processed and pending) from the `endpoints` table into `/home/user/recovered_urls.txt`, with one URL per line.

3. **Bash Remediation**: Modify the `/home/user/uptime-monitor.sh` script. Add a length-checking mechanism in Bash to the script so that it completely skips passing any URL strictly longer than 60 characters to the `check_status` binary. 
   When a URL is skipped, the script must echo exactly `Skipped: <URL>` to stdout. Shorter URLs should continue to be passed to `check_status` as normal.

Ensure all output files are placed exactly at the specified absolute paths.