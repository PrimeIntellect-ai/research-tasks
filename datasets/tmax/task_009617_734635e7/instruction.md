You are a Site Reliability Engineer (SRE) responsible for maintaining an uptime monitoring system. Recently, the primary monitoring script at `/home/user/monitor/uptime_monitor.sh` has stopped working correctly. It is currently failing to report server status and seems to hang indefinitely on certain network failures.

You need to investigate and fix the monitoring system. Here are the symptoms and your objectives:

1. **Database Corruption**: The script uses a flat-file database located at `/home/user/monitor/data/uptime.log` to store daily uptime percentages. However, some corrupted input was written to this file during a sudden disk failure. The script expects every line in this file to exactly match the format `YYYY-MM-DD|FLOAT` (e.g., `2023-10-05|99.9`). Any lines containing garbage characters or not strictly adhering to this format cause the script's reporting mechanism to fail. You must clean `/home/user/monitor/data/uptime.log` by removing only the malformed lines, leaving all valid historical data intact.

2. **Missing Secrets**: The script relies on an API key stored in `/home/user/monitor/config.env`. A junior engineer recently accidentally committed a change that scrubbed this API key from the config file. You must recover the correct `API_KEY` from the git repository's history in `/home/user/monitor` and restore it to `config.env`.

3. **Convergence/Infinite Loop Bug**: A recent update to `/home/user/monitor/uptime_monitor.sh` introduced a logic error in the network retry backoff loop. When a simulated ping fails, the loop is supposed to retry up to 3 times before giving up. Instead, it hangs indefinitely, failing to converge on a terminal state. You must find and fix this bug in the bash script.

Once you have fixed the database, recovered the secret, and patched the script, execute the script by running:
`cd /home/user/monitor && ./uptime_monitor.sh`

If successful, the script will write a final summary to `/home/user/monitor/report.txt`. Your task is complete when `report.txt` is successfully generated and contains the correct "Average Uptime" and "API_STATUS=OK". Do not alter the intended mathematical logic of the script or the valid lines in the database.