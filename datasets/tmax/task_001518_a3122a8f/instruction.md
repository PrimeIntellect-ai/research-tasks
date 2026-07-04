You are tasked with fixing a broken monitoring setup and implementing a missing health-check daemon in C.

Currently, we have a worker process that runs in the background. We need a health monitoring daemon that checks if this worker is alive, and a cron job that periodically records the status. However, the system is incomplete and the existing cron job is writing its output to the wrong place due to environment variable issues.

Please complete the following tasks:

1. **Write a Health Monitor Daemon in C**:
   - Create a C file at `/home/user/healthd.c` and compile it to `/home/user/healthd`.
   - The daemon must read a PID from the file `/home/user/worker.pid`.
   - It should check if that PID is currently running (for example, by checking if `/proc/<PID>/stat` exists).
   - The daemon must listen on TCP port `8080` on `127.0.0.1`.
   - When a client connects, it should send the string `"STATUS: OK\n"` if the process is running, or `"STATUS: FAIL\n"` if it is not. It should then immediately close the connection.
   - Run this daemon in the background.

2. **Fix the Cron Job Environment**:
   - There is a script at `/home/user/query_health.sh` that queries the daemon (e.g., using `nc 127.0.0.1 8080`) and writes the output to `$LOG_DIR/status.log`.
   - The user has set up a cron job to run this script every minute, but because cron executes with a minimal environment, `LOG_DIR` is empty, and it attempts to write to the root directory or fails.
   - Create the directory `/home/user/logs`.
   - Modify the user's crontab (using `crontab -e` or by loading a new crontab file) so that the environment variable `LOG_DIR` is set to `/home/user/logs` for the cron jobs, ensuring the script writes successfully to `/home/user/logs/status.log`.

3. **Start the Worker**:
   - For testing purposes, start a long-running process (like `sleep 3600 &`) and write its PID to `/home/user/worker.pid`.
   - Ensure your daemon is running, and manually run `/home/user/query_health.sh` once with `LOG_DIR=/home/user/logs` to ensure `/home/user/logs/status.log` is populated immediately with `STATUS: OK`.

Your task is complete when the C daemon is compiled, running on port 8080, and correctly identifying the worker process, and the crontab is updated to properly set `LOG_DIR`.