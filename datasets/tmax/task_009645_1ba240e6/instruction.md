You are a monitoring specialist tasked with setting up a health check alert for a backup system. Our backups are stored in `/home/user/backups`, but the monitoring script often fails to find them when executed by our automated scheduler because the scheduler does not set the correct environment variables (like PATH or custom directory variables).

Your task is to create the health check script and a wrapper to ensure it runs correctly regardless of the caller's environment.

Please perform the following steps:
1. Create a directory named `/home/user/backups` if it doesn't exist.
2. Write a Python script at `/home/user/monitor.py`. This script must:
   - Read the target directory from an environment variable named `BACKUP_DIR`.
   - If `BACKUP_DIR` is not set or the directory does not exist, it must exit with status code 2.
   - Look for any file ending in `.bak` inside the directory specified by `BACKUP_DIR`.
   - If at least one `.bak` file exists, print exactly `OK: Backup present` to standard output (stdout) and exit with status code 0.
   - If no `.bak` files exist, print exactly `CRITICAL: Backup missing` to standard error (stderr) and exit with status code 1.
3. Write a shell wrapper script at `/home/user/start_service.sh` that simulates how our daemon will call the script. This wrapper must:
   - Explicitly set and export the `BACKUP_DIR` environment variable to `/home/user/backups`.
   - Execute the `/home/user/monitor.py` script.
   - Redirect all standard output (stdout) from the Python script to `/home/user/monitor.log`.
   - Redirect all standard error (stderr) from the Python script to `/home/user/monitor.err`.
   - Propagate (return) the exact exit code of the Python script as its own exit code.
4. Make sure `/home/user/start_service.sh` is executable.

Do not manually create any `.bak` files yourself. The automated verification system will test your scripts by creating files and running your wrapper.