I am a capacity planner analyzing resource usage for our staging environment. We need a health check and monitoring script that captures storage usage and process health, but our previous cron jobs kept writing logs to the wrong locations because of PATH and working directory differences. 

Please create a Python script at `/home/user/health_monitor.py` that performs the following capacity and health checks:

1. **Storage Monitoring**: Calculate the total size (in bytes) of all files within the `/home/user/app_data/` directory (including subdirectories).
2. **Process Monitoring**: Count the number of currently running processes whose command line contains exactly `background_worker.sh`.
3. **User Check**: Check if a local system user named `deploy_user` exists on the system (by checking `/etc/passwd`).

Your script must write the results as a single JSON object to exactly `/home/user/logs/health.json`. It must use absolute paths to ensure that regardless of which directory the script is executed from, it always checks the correct data directory and writes to the correct log file.

The output in `/home/user/logs/health.json` must be strictly in this JSON format:
```json
{
  "data_size_bytes": 1048576,
  "worker_count": 2,
  "deploy_user_exists": false
}
```

Make sure your script is executable (`chmod +x /home/user/health_monitor.py`) and uses `#!/usr/bin/env python3`. You do not need to set up the cron job itself, just create the robust script and run it once so the `health.json` file is generated for verification.