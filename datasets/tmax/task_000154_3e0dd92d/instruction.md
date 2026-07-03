You are a Site Reliability Engineer investigating recurring 502 Bad Gateway errors on our primary API gateway. The gateway uses Nginx, which proxies to a local UNIX socket (`/run/api-backend/api.sock`) provided by a custom backend service written in C. 

Your investigation and remediation must proceed in three stages:

**Stage 1: Outage Identification (Video Analysis)**
We lost our metrics database, but we have a screen recording of the dashboard during the incident at `/app/dashboard_recording.mp4`. 
The dashboard shows a red square indicator (exactly `#FF0000`) in the top-left 16x16 pixels whenever the 502 error rate exceeds the threshold.
Extract the frames using `ffmpeg`. Identify all seconds in the video where this red square is present. Write these timestamps (one integer per line, representing the second in the video) to `/home/user/outage_seconds.txt`.

**Stage 2: Fix the 502 Upstream Permission Issue**
The Nginx 502 errors persist after backend restarts because the backend daemon (`/opt/backend/api-server`, managed by `api-backend.service`) creates the UNIX socket with restrictive permissions (`root:root` `0755`), preventing the `www-data` Nginx user from connecting.
- Modify the systemd service `/etc/systemd/system/api-backend.service` and/or the initialization scripts it calls so that upon restart, the UNIX socket at `/run/api-backend/api.sock` is accessible by `www-data` (requires `rw` permissions).
- Ensure the service successfully restarts and Nginx can route traffic without a 502. 

**Stage 3: Write a Request Sanitizer (Adversarial Corpus)**
The backend daemon crashes and restarts because of maliciously crafted HTTP headers. We have collected samples of these malicious requests, as well as normal traffic.
Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
This program must read an raw HTTP request from `stdin` until EOF.
- If the request is safe, the program must exit with status `0`.
- If the request is malicious, the program must exit with status `1`.
The malicious requests consistently contain an `X-Trace-Id` header that is longer than 64 characters or contains non-alphanumeric characters (other than hyphens). 
We have provided an evaluation corpus. Your compiled binary will be tested against `/app/corpora/clean/` (which it must accept) and `/app/corpora/evil/` (which it must reject). 

Provide a deployment script at `/home/user/deploy.sh` that restarts Nginx and the backend service gracefully.