You are a Site Reliability Engineer (SRE) tasked with setting up a lightweight uptime monitoring service and its logging infrastructure. 

Perform the following steps:

1. **Mount & fstab processing:**
   Read the file `/home/user/fstab_mock`. Identify the mount point directory associated with the comment `# sre_logs`. Create this directory if it does not already exist.

2. **C Uptime Service:**
   Write a C program at `/home/user/uptime_monitor.c` and compile it to `/home/user/uptime_monitor`.
   The program must:
   - Listen for incoming TCP connections on `127.0.0.1:8080`.
   - Upon accepting a connection, immediately send the following response and close the client socket: `HTTP/1.1 200 OK\r\n\r\nUPTIME_OK`
   - Every time a connection is received, append exactly one log line to `<mount_point_from_step_1>/uptime.log`.
   - The log line MUST strictly follow this format: `[YYYY-MM-DD HH:MM:SS JST] SYSTEM_UP\n`
   - Important: The timestamp in the log must be in the `Asia/Tokyo` timezone. You must configure this *programmatically* within your C code (e.g., overriding the environment variables for the process) so that it logs JST time regardless of the system's default locale and timezone.
   
   Start your compiled `uptime_monitor` in the background.

3. **SSH Tunneling:**
   The host has an SSH server running, and passwordless localhost SSH is already configured for your user.
   Set up a background local SSH port forward that forwards local port `9090` to `127.0.0.1:8080` over an SSH connection to `localhost`.

4. **Testing:**
   Using `curl`, make exactly 5 requests to `http://127.0.0.1:9090`. Do this slowly enough (e.g., 1 second apart) to ensure proper timestamps.

5. **Log Rotation:**
   Create a logrotate configuration file at `/home/user/logrotate.conf` that manages `<mount_point_from_step_1>/uptime.log`. 
   Configure it to:
   - Rotate the log file daily, or if it exceeds `10 bytes` (which our 5 lines will).
   - Keep 3 rotated backups.
   - Truncate the original log file in place (`copytruncate`).
   
   Execute `logrotate` manually using your configuration file (use `/home/user/logrotate.status` as the state file) and force a rotation.

6. **Verification:**
   Count the number of log lines in the newly rotated backup file (which should be named `uptime.log.1` by default). Write this integer to `/home/user/result.txt`.