You need to create a lightweight, local "operator" script in Python that manages log configurations for simulated container deployments. 

We have a scheduling wrapper that will run your script, but due to a known bug in our custom cron implementation, the script is executed with a completely random working directory (e.g., `/tmp` or `/var/tmp`). Your script must handle paths robustly and not rely on the current working directory.

Please write a Python script at `/home/user/manifest_operator.py`.

Requirements for `/home/user/manifest_operator.py`:
1. It must read the desired container state from exactly `/home/user/desired_state.json`.
2. The JSON file will have the following structure:
   ```json
   {
     "containers": [
       {"name": "frontend", "log_dir": "/home/user/logs/frontend"},
       {"name": "backend", "log_dir": "/home/user/logs/backend"}
     ]
   }
   ```
3. For every container listed in the JSON:
   - Ensure the specified `log_dir` directory exists (create it if it does not).
4. Generate a single logrotate configuration file at `/home/user/generated_logrotate.conf`.
   - The script must be idempotent: running it multiple times should result in the exact same file content, without duplicate entries. (The easiest way is to rewrite the file based solely on the current JSON state).
   - For each container, append the following exact logrotate block format to the file (replace the path with the container's `log_dir`):
   ```text
   <log_dir>/*.log {
       daily
       rotate 7
       compress
       missingok
       notifempty
   }
   ```
   Leave exactly one blank line between container blocks.
5. Your script should not require root privileges.
6. Remember, your script will be tested by invoking it from a completely different directory, so use absolute paths for the hardcoded file locations mentioned above.

To complete the task, write the script and run it at least once so the directories and the `/home/user/generated_logrotate.conf` file are created.