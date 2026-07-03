I am an SRE setting up a local uptime monitoring pipeline. We have a test environment running multiple services, but the automated monitoring workflow is currently broken due to misconfigurations, bad permissions, and a missing parsing component.

Here is the current architecture running under `/app/`:
1. **Redis** running on `localhost:6379`.
2. **Aggregator API** (Flask) running on `localhost:5000`.
3. **Target SSHd** running locally as the current user on port 2222. It generates simulated heartbeat logs at `/app/logs/heartbeat.log`.

Your objectives are to fix the infrastructure and write a log parsing script that perfectly mimics our legacy reference implementation.

### Phase 1: Fix the Service Configuration and Permissions
A synchronization script located at `/home/user/monitor_sync.sh` is supposed to use `scp` to fetch `/app/logs/heartbeat.log` via the local SSH daemon on port 2222 using the key `/home/user/.ssh/monitor_key`. 
Currently, the SSH daemon silently rejects this key-based login. 
1. Identify and fix the permissions/ACLs or SSH configuration preventing the key from working. The key must authenticate to `localhost` on port `2222` without prompting for a password.
2. Set up a user `cron` job that executes `/home/user/monitor_sync.sh` every minute.

### Phase 2: Write the Log Parser (`/home/user/log_parser.py`)
The `monitor_sync.sh` script pipes the fetched log file into `/home/user/log_parser.py`. You must create this Python script. 
It must read line-by-line from `stdin`. Each line of the log has the format:
`[UNIX_TIMESTAMP] <SERVICE_NAME> <EVENT>`
*Example:* `[1710000000] frontend HEARTBEAT_OK`

Valid events are exactly `HEARTBEAT_OK` or `HEARTBEAT_FAIL`. Ignore any line that does not perfectly match this format or has an unrecognized event. Also, ignore any line where the `UNIX_TIMESTAMP` is strictly *less than* the timestamp of the previously processed valid line for that specific `<SERVICE_NAME>` (chronological violations).

The script must print to `stdout` a summary in CSV format with exactly the following header:
`SERVICE_NAME,TOTAL_OK,TOTAL_FAIL,MAX_CONSECUTIVE_OK`

Rules for the output:
1. One row per discovered valid `<SERVICE_NAME>`.
2. `TOTAL_OK` is the count of `HEARTBEAT_OK` events.
3. `TOTAL_FAIL` is the count of `HEARTBEAT_FAIL` events.
4. `MAX_CONSECUTIVE_OK` is the longest unbroken sequence of `HEARTBEAT_OK` events for that service.
5. Sort the rows alphabetically by `SERVICE_NAME` (ascending).

We have a compiled reference oracle at `/app/oracle_parser` that implements this exact logic. Your Python script must produce bit-exact identical output to the oracle for *any* sequence of log inputs.

Finally, ensure all services are running and the end-to-end flow works: `/home/user/monitor_sync.sh` must be able to run successfully, parse the log, and submit the parsed metrics to the Aggregator API.