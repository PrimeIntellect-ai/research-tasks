You are a monitoring specialist tasked with configuring an alert generation and sanitization pipeline for a data center.

Your task consists of three parts.

**Part 1: Video Anomaly Detection**
A security camera has captured footage of a server rack. The video file is located at `/app/rack_monitor.mp4`. 
Recently, a hardware fault caused a red warning light to flash on one of the servers.
1. Extract the frames from this video at 1 frame per second using `ffmpeg` (save them to `/home/user/frames/`).
2. Write a bash script or C++ program to analyze these extracted frames. You need to identify frames that contain significant bright red pixels (where Red > 200, Green < 50, and Blue < 50).
3. Output the exact timestamps (in seconds, matching the frame number) of the anomalous frames to a text file at `/home/user/red_alert_timestamps.txt`, one timestamp per line.

**Part 2: Webhook Sanitizer**
Our alert system receives JSON payloads via a reverse proxy. However, we have detected path traversal attacks targeting our filesystem configuration (specifically attempting to overwrite fstab or access linked logging directories).
1. Write a C++ program at `/home/user/alert_filter.cpp` and compile it to `/home/user/alert_filter`.
2. The program must accept a single command-line argument: the path to a text file containing an alert payload.
   Example: `./alert_filter /path/to/payload.json`
3. The program must analyze the file's contents and exit with code `0` if the payload is safe (clean), and exit with code `1` if the payload contains path traversal patterns (e.g., `../`, `..%2F`, or null bytes) or unusually long string payloads (over 1000 characters) that might be buffer overflow attempts.

**Part 3: Filesystem & Vault Setup**
We need a secure, isolated storage area for these alerts.
1. Create a 50MB empty file at `/home/user/vault.img` and format it as an `ext4` filesystem.
2. Create a mount point directory at `/home/user/vault_mount`.
3. Create a directory structure for the reverse proxy cache at `/home/user/proxy_cache/` with three subdirectories: `alerts`, `metrics`, and `logs`.
4. Create a symlink so that `/home/user/proxy_cache/alerts` points to `/home/user/vault_mount/alerts`. (Assume the `alerts` folder will exist once mounted).
5. Write the exact `fstab` configuration line required to mount `/home/user/vault.img` at `/home/user/vault_mount` with `ext4` using the `loop` option. Save ONLY this single line to `/home/user/vault_fstab`.

Ensure all code compiles successfully and files are placed exactly at the requested paths.