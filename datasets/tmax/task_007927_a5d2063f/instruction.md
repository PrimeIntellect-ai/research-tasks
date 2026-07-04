You are a Site Reliability Engineer (SRE) taking over an internal uptime monitoring system that has recently failed. The system is written in Bash and relies on SQLite for data storage. Your goal is to diagnose and fix several interconnected issues: build failures, corrupted input handling, incorrect database queries, a race condition, and a lost API credential.

The workspace is located at `/home/user/monitor_app/`.

Here are your tasks:

1. **Git History Forensics (Secret Recovery)**
   The alerting service relies on a third-party ping API, but the developer accidentally removed the API key from the configuration repository and committed the change. 
   - Inspect the Git repository located at `/home/user/monitor_app/config_repo/`.
   - Find the deleted `API_KEY` value in the git history.
   - Create a file at `/home/user/monitor_app/secrets.env` containing exactly the recovered line: `API_KEY=the_value_you_found`.

2. **Build Failure Diagnosis**
   The installation script `/home/user/monitor_app/build.sh` is failing to execute. 
   - Debug and fix the syntax errors in `build.sh`.
   - Identify and install any missing dependencies locally or modify the script to work. (You have `sudo apt-get` privileges if package installation is strictly required, though local fixes are preferred).
   - Once fixed, run `./build.sh`. It is designed to create `/home/user/monitor_app/build_success.log` if it completes successfully.

3. **Corrupted Input Handling & Query Debugging**
   The service reads raw ping logs from `/home/user/monitor_app/uptime_logs.txt`. Recently, the log generator started outputting corrupted, malformed lines alongside valid ones.
   - The script `/home/user/monitor_app/ingest.sh` is supposed to parse these logs and insert valid records into an SQLite database (`/home/user/monitor_app/uptime.db`), and then output the total count of successful pings (HTTP 200).
   - Currently, `ingest.sh` crashes on corrupted lines, and its SQLite query to count successful pings is fundamentally flawed.
   - Modify `ingest.sh` to safely skip lines that do not match the format `TIMESTAMP HTTP_STATUS` (where TIMESTAMP is an integer and HTTP_STATUS is a 3-digit integer).
   - Fix the SQLite query inside `ingest.sh` so it accurately counts and prints the number of rows where the status is exactly `200`.
   - Run the fixed `ingest.sh`. It will output a number. Save this exact number to `/home/user/monitor_app/query_result.txt`.

4. **Race Condition Debugging**
   The alert system uses `/home/user/monitor_app/alert.sh` to track consecutive failures by incrementing a counter in `/home/user/monitor_app/alert_state.txt`. 
   - Currently, if `alert.sh` runs concurrently, it suffers from a race condition and loses counts.
   - Fix `/home/user/monitor_app/alert.sh` by introducing file locking (e.g., using `flock`) so that concurrent executions safely increment the counter.
   - To test your fix, run `/home/user/monitor_app/run_alerts_test.sh`. It will spawn 50 background processes of `alert.sh`. If your lock is implemented correctly, `/home/user/monitor_app/alert_state.txt` will contain exactly `50` at the end.

Ensure all outputs are exactly at the specified paths. Do not change the names of the final verification files.