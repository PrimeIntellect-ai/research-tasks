You are an edge computing engineer deploying a new IoT surveillance node. You need to configure the node to process a local video feed, handle incoming control messages securely, and manage its system resources. 

Perform the following tasks as the standard user (no root access required):

1. **Link and Directory Management:**
   - Create a directory `/home/user/frames/`.
   - Create a symlink at `/home/user/active_feed.mp4` pointing to the system's video feed located at `/app/camera1.mp4`.

2. **Video Processing (Process Control):**
   - Use `ffmpeg` to extract frames from `/home/user/active_feed.mp4` into the `/home/user/frames/` directory at a rate of exactly 1 frame per second. Name the output files `frame_%04d.jpg`. Keep this process lightweight; exit once extraction is complete.

3. **Port Forwarding:**
   - Set up user-space port forwarding using `socat` to forward all incoming TCP traffic on port `8080` to TCP port `9090` on localhost. Run this in the background and leave it running.

4. **Payload Validator (Python Scripting & Locale/Timezone):**
   - The IoT device receives JSON control payloads via standard input. Write a Python script at `/home/user/validator.py` to validate these payloads.
   - The script must read a single JSON payload from `stdin`.
   - The payload contains three fields: `"action"`, `"device_id"`, and `"tz"` (timezone).
   - **Accept condition (exit code 0):** `"action"` is exactly `"capture"`, `"device_id"` is strictly alphanumeric (1-20 characters), and `"tz"` matches standard IANA timezone formats (e.g., "America/New_York", "UTC", matching the regex `^[A-Za-z_]+(/[A-Za-z_]+)?$`).
   - **Reject condition (exit code 1):** The payload is not valid JSON, `"device_id"` contains any shell metacharacters (potential command injection), or `"tz"` contains path traversal sequences (e.g., `../`).
   - The script must append the raw JSON of accepted payloads to `/home/user/logs/valid.log` and rejected payloads to `/home/user/logs/rejected.log`.

5. **Log Configuration and Rotation:**
   - Create a local logrotate configuration file at `/home/user/logrotate.conf`.
   - Configure it to rotate all `.log` files in `/home/user/logs/` daily, keep 7 days of backlogs, compress rotated files, and create new empty log files with `0644` permissions.