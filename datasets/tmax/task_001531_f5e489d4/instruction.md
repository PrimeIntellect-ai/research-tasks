You are a network engineer troubleshooting a connectivity and storage issue for an internal application. A backend service is configured to run on port 8080, but legacy clients are hardcoded to connect to port 9090. Furthermore, the previous port forwarding solution had no log management, which caused the disk quota to fill up and crash the system.

Your task is to implement a robust, Python-based networking and monitoring solution entirely in user-space.

Please write three separate Python scripts in `/home/user/` to resolve this:

1. **The Port Forwarder (`/home/user/port_forwarder.py`)**:
   Write a Python script that listens on TCP `127.0.0.1:9090`. When a connection is received, it must:
   - Establish a connection to `127.0.0.1:8080`.
   - Forward data bidirectionally between the client and the backend service.
   - Append the exact string `FORWARD_SUCCESS` on a new line to the file `/home/user/logs/traffic.log` every time a new connection is accepted.
   *(Note: The script should be able to handle multiple sequential connections, though concurrency is not strictly required for this test. Use only Python standard libraries.)*

2. **The Log Rotator (`/home/user/log_manager.py`)**:
   Write a Python script that implements manual log rotation. When executed, it must check the size of `/home/user/logs/traffic.log`.
   - If the file size is strictly greater than `1024` bytes, it must rename `traffic.log` to `traffic.log.1` (overwriting `traffic.log.1` if it already exists).
   - It must then create a new, empty `/home/user/logs/traffic.log` file.
   - If the file is 1024 bytes or smaller, do nothing.

3. **The Quota Monitor (`/home/user/quota_check.py`)**:
   Write a Python script that calculates the total size (in bytes) of all files inside the `/home/user/logs/` directory.
   - It must write the result to `/home/user/quota_report.txt` in the exact format: `TOTAL_BYTES: <size_in_bytes>`
   - For example, if the directory contains 1500 bytes of data, the file should contain exactly: `TOTAL_BYTES: 1500`

**Pre-requisites you must ensure:**
- Create the `/home/user/logs/` directory before starting your scripts.
- Ensure all Python scripts are executable or can be run directly via `python3`.

Do not run the forwarder as a daemon; the automated test will launch your scripts directly to verify their behavior.