You are assisting a network engineer in setting up an automated connectivity troubleshooting tool. The engineer needs a scheduled job that monitors local ports, rotates its own log files to conserve disk space, and maintains a stable pointer to the most recent results.

Your task is to implement this system by following these requirements:

1. Create a log directory at `/home/user/logs`.
2. Write a Python script at `/home/user/net_monitor.py`. The script must perform the following actions exactly in this order:
   - **Storage Monitoring & Rotation**: Calculate the total size (in bytes) of all regular files (excluding symlinks) inside `/home/user/logs`. If the total size is greater than or equal to 100 bytes, delete the oldest regular file(s) in the directory (based on modification time) until the total size is strictly less than 100 bytes.
   - **Network Check**: Read a list of ports from `/home/user/ports.txt` (one integer per line). For each port, attempt a TCP connection to `127.0.0.1` on that port with a 1-second timeout.
   - **Logging**: Create a new log file in `/home/user/logs/` named `run_<UNIX_TIMESTAMP>.log` (where `<UNIX_TIMESTAMP>` is the current integer epoch time, e.g., `run_1690000000.log`). Write the status of each port to this file, one per line, sorted numerically by port. The format must be exactly `PORT <port>: UP` or `PORT <port>: DOWN`.
   - **Link Management**: Create or update a symbolic link at `/home/user/logs/latest.log` to point to the newly created log file. Ensure the symlink is a relative link (pointing to the filename within the same directory).

3. Schedule the task:
   - Create a crontab entry for the current user that runs `python3 /home/user/net_monitor.py` every minute.

4. To test your script and ensure log rotation works properly, run your script manually 4 times, pausing for at least 1 second between each execution (to ensure unique timestamps).

**Environment Details:**
- The list of ports is already provided in `/home/user/ports.txt`.
- Some background services are already listening on some of these ports.