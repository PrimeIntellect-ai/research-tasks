You are a monitoring specialist investigating a series of silent connection rejections occurring on our edge nodes, reminiscent of an SSH configuration silently dropping key-based logins. Your goal is to extract evidence from a screencast, write a robust log filter to detect these drops, and set up a containerized secure web server to host your findings.

Please perform the following steps:

1. **Storage Mounting & Diagnostics**:
   An ext4 filesystem image is located at `/app/evidence.img`. Mount this image to `/mnt/evidence`. Ensure this mount persists across reboots by adding an entry to `/etc/fstab` (assume you have sudo access for the fstab edit and mounting, via `sudo mount`). Inside this mount, you will find connectivity logs and a diagnostic video. 

2. **Video Analysis**:
   The mounted directory contains a video file `/mnt/evidence/network_status.mp4`. This video records a hardware monitoring dashboard. A silent connection drop is indicated by the dashboard screen flashing pure red (RGB: 255, 0, 0) for exactly one frame. 
   Use `ffmpeg` (which is pre-installed) to analyze this video. Count the exact number of red frames. Write this integer count to `/home/user/drop_count.txt`.

3. **Log Filter / Classifier**:
   Write an executable script at `/home/user/classify_logs.py` (or `.sh`, model's choice). This script must read a log file path as its first CLI argument and print either `EVIL` or `CLEAN` to standard output.
   - A log file is considered `EVIL` if it contains 3 or more entries indicating a silent drop (Status Code `499` originating from the IP subnet `10.99.x.x`). 
   - Otherwise, it is `CLEAN`.
   Your script will be tested against a hidden corpus of clean and evil logs.

4. **Web Server & Containerization**:
   Deploy an Nginx web server running inside a Docker/Podman container. 
   - The container must be named `alert-web`.
   - It must bind to port `8443` on the host.
   - You must configure it to serve HTTPS traffic using a self-signed TLS certificate (place the certs in `/home/user/certs/`).
   - The default web root must serve a file named `index.html` containing the word `CRITICAL_ALERT` followed by the number of red frames you found in the video (e.g., `CRITICAL_ALERT: 42`).

Ensure all scripts are executable and the Nginx container remains running in the background.