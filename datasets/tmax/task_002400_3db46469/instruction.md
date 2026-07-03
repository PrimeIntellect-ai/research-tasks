You are a Site Reliability Engineer (SRE) responsible for maintaining a legacy uptime monitoring system written in Bash. 

The primary monitoring script, located at `/home/user/monitor_daemon.sh`, reads a list of endpoints from `/home/user/endpoints.txt` and checks their health. Recently, an issue was introduced: when the script encounters a certain type of failing endpoint, it enters an infinite recursion loop due to a flawed retry algorithm. This fills up the logs at `/home/user/monitor.log`, hangs the monitoring process, and prevents the script from finishing its run and writing to `/home/user/status.log`.

Your tasks are:
1. **Log Analysis & Test Minimization:** The `endpoints.txt` file contains many endpoints. Use delta debugging or binary search techniques to identify the single specific endpoint URL in `endpoints.txt` that consistently triggers the infinite recursion loop.
2. **Algorithmic Fix:** Modify `/home/user/monitor_daemon.sh` to fix the infinite recursion bug. Implement a proper loop or recursion termination condition that limits the retry attempts to exactly **3 retries** per failing endpoint. If it still fails after 3 retries, it should log the failure and continue to the next endpoint.
3. **Validation:** Run your fixed `/home/user/monitor_daemon.sh` script against the original `/home/user/endpoints.txt`. The script must successfully check all endpoints, terminate normally, and output "MONITORING COMPLETE" to `/home/user/status.log`.
4. **Reporting:** Create a report file at `/home/user/resolution.txt` with exactly two lines:
   - Line 1: The exact URL of the problematic endpoint that triggered the bug.
   - Line 2: The text `FIXED`

Ensure that you have started any required background services if the daemon expects local services to be running (e.g., checking if there's a local mock server script provided in the home directory).