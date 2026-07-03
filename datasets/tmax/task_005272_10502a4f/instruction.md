You are a Site Reliability Engineer responsible for bridging a legacy hardware monitoring system with a modern observability stack. 

The legacy system outputs its status by changing the color of an LED, which is being recorded by a camera. We have a clip of this recording located at `/app/server_status.mp4`. 

Your goal is to extract the downtime events from this video, build a C++ metric exporter, and securely expose it behind a reverse proxy.

Complete the following tasks:

1. **Video Analysis (Connectivity / Status Diagnostics)**
   Analyze the video file `/app/server_status.mp4` using `ffmpeg` and bash tools. The video shows a solid color that is normally green but occasionally flashes pure red. Calculate the exact number of distinct times the video flashes red (downtime events).

2. **Metric Exporter (C++)**
   Write a C++ program at `/home/user/gateway.cpp` and compile it to `/home/user/gateway`. 
   The program must act as a lightweight HTTP server listening on `127.0.0.1:8080`.
   - It must handle `GET /metrics` requests.
   - It must require an exact HTTP header: `Authorization: Bearer SRE-SECRET-TOKEN`. If this is missing or incorrect, return `HTTP/1.1 401 Unauthorized`.
   - If authorized, return `HTTP/1.1 200 OK` with the body containing a single line: `downtime_events_total <COUNT>`, where `<COUNT>` is the integer number of red flashes you found in the video.

3. **Secure Web Server & Log Rotation (Idempotent Bash Scripting)**
   Write an idempotent bash script at `/home/user/setup_gateway.sh` that performs the following without requiring `sudo` or `root`:
   - Generates a self-signed TLS certificate and private key in `/home/user/certs/`.
   - Creates a user-space Nginx configuration file at `/home/user/nginx.conf`.
   - The Nginx server must listen on `127.0.0.1:8443` with TLS enabled, using the generated certificates.
   - It must proxy all requests to your C++ backend at `http://127.0.0.1:8080`.
   - It must configure Nginx to write access logs to `/home/user/logs/access.log` and error logs to `/home/user/logs/error.log`.
   - It must create a valid `logrotate` configuration file at `/home/user/logrotate.conf` that targets the `/home/user/logs/access.log`, rotating it daily, keeping 3 backups, and compressing them.
   - The script should start Nginx (e.g., `nginx -p /home/user -c /home/user/nginx.conf`) and restart it cleanly if the script is run multiple times.

4. **Execution**
   Run your C++ backend in the background and execute your setup script so that the HTTPS endpoint on port 8443 is live and operational. Do not stop the processes; they must remain running for the automated verification.