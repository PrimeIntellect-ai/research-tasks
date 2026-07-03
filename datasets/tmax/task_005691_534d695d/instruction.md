I set up a scheduled job to monitor my local mailing list SMTP server, but I'm running into an issue. When I run the monitoring script (`/home/user/app/mail_monitor.py`) directly from my terminal, it works perfectly. However, when my scheduler runs it, it crashes or writes the logs to completely unpredictable locations because of environment variable and PATH differences.

I need you to fix this monitoring setup. Here is what you need to do:

1. **Fix the Python Script (`/home/user/app/mail_monitor.py`)**:
   - The script currently relies on the `SMTP_SERVER_IP` environment variable which is set in my interactive shell but missing in the scheduler. Modify the script so it uses robust error handling. If `SMTP_SERVER_IP` is missing, it should default to `127.0.0.1`.
   - The script currently attempts to write to a relative path `report.log`. Change this so it always writes to an absolute path: `/home/user/app/output/report.log`. Create the `output` directory if it does not exist.
   - Implement the actual connectivity diagnostic: The script must use Python's `smtplib` to attempt a connection to the SMTP server on port `10255`. 
   - If the connection succeeds, append the exact string `STATUS: OK` on a new line to `/home/user/app/output/report.log`.
   - If the connection fails (e.g., connection refused), catch the exception gracefully and append `STATUS: ERROR` to the log file instead.

2. **Create a Robust Shell Wrapper (`/home/user/app/run_monitor.sh`)**:
   - Write a bash script that the scheduler can call safely.
   - It must explicitly export `SMTP_SERVER_IP="127.0.0.1"`.
   - It must execute the Python script `/home/user/app/mail_monitor.py`.
   - Ensure the shell script is executable.

To verify your solution, execute your wrapper script `/home/user/app/run_monitor.sh` manually once so that it generates the `/home/user/app/output/report.log` file. I will check this log file to confirm the diagnostic succeeded.