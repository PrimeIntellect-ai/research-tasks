You are a container specialist managing a migration for legacy microservices. Before fully containerizing them, you need to standardize their environment (locale and timezone) and implement a robust process monitoring and backup script.

Three microservice scripts exist in `/home/user/services/`:
1. `auth.py`
2. `data.py`
3. `web.py`

Each service stores its active state in a corresponding directory: `/home/user/data/auth/`, `/home/user/data/data/`, and `/home/user/data/web/`.

Your task is to write a Python process monitor and orchestrate a deployment test.

**Step 1: Write the Deployment Monitor**
Create a Python script at `/home/user/deploy_monitor.py` that fulfills these requirements:
- When executed, it launches all three service scripts (`auth.py`, `data.py`, `web.py`) as background processes.
- **Environment constraints:** Each process MUST be launched with specific environment variables: `TZ=UTC` and `LC_ALL=C.UTF-8`.
- **Monitoring & Backup:** The script must continuously monitor the health of these 3 child processes (checking every 1 second). 
- If any process terminates or is killed, the monitor must immediately:
  1. Create a gzip-compressed tarball of the crashed service's data directory. Save it exactly as `/home/user/backups/<service_name>_backup.tar.gz` (e.g., `auth_backup.tar.gz`).
  2. Restart the service with the same required environment variables (`TZ` and `LC_ALL`).

**Step 2: Execute and Test**
1. Ensure the directories `/home/user/backups/` and the data directories exist.
2. Run your `deploy_monitor.py` script in the background.
3. Simulate a crash by manually killing the `auth.py` process.
4. Wait for your monitor to detect the crash, perform the backup, and restart `auth.py`.

**Step 3: Verification Report**
Finally, create a JSON file at `/home/user/deployment_report.json` containing the current state of the system after the test. It must exactly match this structure:

```json
{
  "auth_restarted": true,
  "backups_created": ["auth_backup.tar.gz"],
  "active_pids": {
    "auth": <new_pid_of_auth>,
    "data": <pid_of_data>,
    "web": <pid_of_web>
  }
}
```
*(Replace the `<pid>` placeholders with the actual integer process IDs currently running.)*