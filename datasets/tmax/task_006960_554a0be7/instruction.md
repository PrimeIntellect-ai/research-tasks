You are an infrastructure engineer automating the provisioning and monitoring of a lightweight deployment. We have a critical local service that processes data, and we need a robust script to monitor its health and secure its data if it crashes.

Your task is to implement the following:

1. Environment Setup:
   - Add the environment variable `export MONITOR_MODE=automated` to the end of the `/home/user/.bashrc` file.

2. Python Monitoring Script:
   - Write a Python script at `/home/user/service_monitor.py`.
   - The script must read the environment variable `MONITOR_TARGET_PID` to get the process ID of the target service.
   - The script must check if the process with that PID is currently running (e.g., by checking `/proc/<pid>`).
   - If the process IS running:
     - Append the exact string `[OK] Service running.` on a new line to `/home/user/monitor.log`.
     - Exit cleanly with status code 0.
   - If the process IS NOT running (or the PID doesn't exist):
     - Create a compressed tarball (`.tar.gz`) of the entire directory `/home/user/app_data/` and save it to `/home/user/backup.tar.gz`. Handle errors robustly.
     - Append the exact string `[CRITICAL] Service down. Backup created.` on a new line to `/home/user/monitor.log`.
     - Exit cleanly with status code 0.

Ensure your Python script is robust, properly handles cases where the environment variable is missing (it should exit with code 1 in that case), and correctly identifies running vs. dead processes.