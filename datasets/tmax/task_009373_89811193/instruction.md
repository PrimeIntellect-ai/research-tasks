You are an observability engineer trying to tune local filesystem monitoring dashboards. 

A legacy administration daemon running on this server exposes critical health paths, but it is bound exclusively to a UNIX domain socket at `/home/user/admin.sock`. Your new dashboard tool can only perform health checks over TCP.

Your task is to bridge this gap and extract the filesystem metrics:

1. **Port Forwarding:** Create a local port forward that listens on TCP port `9090` (localhost) and forwards all traffic to the UNIX domain socket `/home/user/admin.sock`. You may use tools like `socat` (if installed) or write a short Python proxy script to accomplish this in the background.
2. **Interactive Automation (Expect):** The daemon requires interactive authentication. Write an automation script (using standard `expect` or Python's `pexpect`/socket automation) named `/home/user/health_check.py` or `/home/user/health_check.exp`. When executed, this script must:
   - Connect to `127.0.0.1` on port `9090`.
   - Wait for the prompt: `Passcode:`
   - Send the password: `obs_secure_123`
   - Wait for the prompt: `Action:`
   - Send the command: `CHECK_FS`
   - Capture the output, which will be a single absolute directory path (e.g., `/home/user/logs_dir`).
3. **Filesystem Monitoring:** Write a Python script named `/home/user/dashboard.py` that:
   - Executes your interactive automation script from step 2 to retrieve the target directory path.
   - Calculates the total byte size of all files recursively within that returned directory path.
   - Writes the final result to `/home/user/dashboard_result.txt` in exactly this format:
     `Target: <directory_path>, Size: <total_bytes>`

Requirements:
- Ensure the port forwarding process is running so the connection succeeds.
- The `dashboard.py` script should handle extracting the path cleanly from whatever output your expect script produces.
- Do not use root privileges (you do not have `sudo`). Use local/user-space tools or Python scripts.