You are a system administrator responsible for maintaining a telemetry processing pipeline. Currently, the Nginx reverse proxy routing traffic to our telemetry daemon is returning a "502 Bad Gateway" error because the backend daemon frequently crashes when receiving malformed or malicious payloads.

Your objective is to fix the pipeline, implement an input sanitizer in C, set up process supervision, and extract diagnostic metadata from an incident video.

Here are your tasks:

1. **Video Analysis for Diagnostics:**
   An incident was recorded in `/app/incident_record.mp4`. We need to know how many times the camera feed dropped out.
   Extract frames from the video at 1 frame per second (using `ffmpeg`). Determine how many of those extracted frames are completely black (all pixels are #000000 or close to 0 intensity). Write this exact integer count to `/home/user/black_frame_count.txt`.

2. **Develop a Payload Sanitizer (C):**
   The backend crashes due to specific malicious telemetry payloads. We have isolated examples of good and bad payloads.
   - Clean payloads are stored in `/app/corpora/clean/`.
   - Malicious (crashing) payloads are stored in `/app/corpora/evil/`.
   
   Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. 
   The program must read a payload from standard input (`stdin`).
   - If the payload is "clean", it must output the exact payload to `stdout` and exit with code `0`.
   - If the payload is "evil" (contains SQL injection signatures like `DROP TABLE`, or buffer overflow attempts like strings exceeding 1000 'A' characters, or invalid JSON brackets), it must exit with a non-zero exit code (e.g., `1`) and output nothing.

3. **Process Supervision & Nginx Fix:**
   - The original telemetry daemon is located at `/app/backend/telemetry_daemon` (which listens on port 8080).
   - Create a bash-based watchdog script at `/home/user/watchdog.sh` that continuously restarts `/app/backend/telemetry_daemon` if it crashes.
   - Nginx is already installed. Fix its configuration at `/etc/nginx/sites-enabled/default` so that it acts as a reverse proxy for the daemon, but only forwards requests that pass your `/home/user/sanitizer`. (You may use an intermediate FastCGI wrapper or a small bash CGI script utilizing `nc` to bridge Nginx, your sanitizer, and the daemon). 

You have full bash access. Provide your solution by modifying the system state as requested. Nginx must be running and returning 200 OK for valid payloads sent to `http://localhost:80/telemetry` when you are finished.