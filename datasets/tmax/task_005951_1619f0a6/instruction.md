You are an IT monitoring specialist. We need to set up a filesystem alerting pipeline for a critical data directory. 

Your task is to create a complete, automated monitoring setup by following these requirements exactly:

1. **Environment Configuration**:
   Create a file at `/home/user/monitor_env.sh` that exports the following environment variables:
   - `MONITOR_DIR=/home/user/data_drop`
   - `SIZE_LIMIT=5000` (in bytes)
   - `ALERT_MAILBOX=/home/user/alerts.mbox`
   Make sure to create the `/home/user/data_drop` directory.

2. **Legacy System Registration (Expect Script)**:
   There is a mock legacy registration tool at `/home/user/bin/register_node.py` (which we will assume is already placed there by the system). When executed, it interactively asks:
   - `Enter node name: ` (You should answer: `worker-01`)
   - `Enter auth token: ` (You should answer: `secret-token-99`)
   Write an Expect script at `/home/user/register.exp` that automates this interaction and runs `/home/user/bin/register_node.py`. The script must print "Registration successful" and exit with 0 when successful.

3. **Python Filesystem Monitor**:
   Write a Python script at `/home/user/monitor.py` that does the following:
   - Sources the environment variables from `/home/user/monitor_env.sh` (or assumes they are loaded in the environment).
   - Scans all files in the `MONITOR_DIR`.
   - If it finds any file strictly larger than `SIZE_LIMIT` bytes, it writes an email alert to the `ALERT_MAILBOX` in standard `mbox` format.
   - The email must have the subject `ALERT: Large file detected - <filename>` (where <filename> is the basename of the file).
   - State Tracking: To avoid duplicate alerts, the script must maintain a JSON state file at `/home/user/monitor_state.json`. If an alert has already been generated for a specific file (identified by its absolute path), it should not generate another alert for that file even if it continues to exist.

4. **Idempotent Setup Script**:
   Write a Bash script at `/home/user/setup.sh` that ties everything together:
   - It must be completely idempotent (safe to run multiple times without causing errors or duplicate entries).
   - It must create `/home/user/monitor_env.sh`, `/home/user/register.exp`, and `/home/user/monitor.py` as specified above.
   - It must run the `/home/user/register.exp` script successfully.
   - It must set up a user-level `cron` job that executes `/home/user/monitor.py` every 1 minute. The cron job must load the variables from `/home/user/monitor_env.sh` before running the python script.

Ensure all paths are absolute and the scripts have the correct execute permissions. Your final goal is to just write the `/home/user/setup.sh` script, which when executed, will create all necessary files, configure cron, and register the node.