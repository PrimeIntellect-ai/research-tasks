You are a network engineer troubleshooting connectivity issues with a local QEMU VM's VNC service. You need to create an automated, idempotent Python monitoring script that checks TCP connectivity to the VNC port and maintains a rotated log of the results.

Please perform the following steps:

1. Create a directory at `/home/user/vnc_logs` to store the monitoring logs.
2. Write a Python script at `/home/user/vnc_monitor.py`. This script must:
   - Attempt a TCP socket connection to `127.0.0.1` on port `5900` with a 2-second timeout.
   - Configure a logger named `vnc_logger` using Python's built-in `logging` and `logging.handlers.RotatingFileHandler`.
   - The log file must be saved at `/home/user/vnc_logs/monitor.log`.
   - The rotation policy must restrict the file size to a maximum of `60` bytes, keeping up to `3` backup files (`backupCount=3`).
   - The log formatter must use exactly this format string: `%(asctime)s - VNC_STATUS - %(message)s`
   - If the TCP connection is successful (socket connects), log the exact message: `SUCCESS`
   - If the TCP connection fails (ConnectionRefused, Timeout, etc.), log the exact message: `FAILED`
3. Make sure your Python script is idempotent (running it multiple times should not infinitely stack file handlers if it were imported, though for this task running it as a standalone script is fine).
4. Execute your script exactly 5 times sequentially (e.g., using a simple shell loop) to populate the logs and trigger the log rotation mechanism. 

Make sure the final state of `/home/user/vnc_logs` contains the base log and its rotated backups.