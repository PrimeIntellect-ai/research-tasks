You are a container specialist managing an edge microservices deployment. Your task is to implement a Video Anomaly Microservice written in C, along with its deployment configuration. 

You must complete the following requirements:

1. **Permissions and Environment Setup:**
   - Create a directory `/home/user/app_data`.
   - Set the ACL of `/home/user/app_data` so that the user `user` has full read/write/execute permissions, but any newly created files inside inherit an ACL where the group `users` has read-only access and `others` have absolutely no access.
   - Create a log directory `/home/user/logs` with the same ACL requirements.

2. **Video Processing Service (C Programming):**
   - Write a C program at `/home/user/src/video_server.c`.
   - The program must analyze the video file located at `/app/camera_feed.mp4`.
   - Using `ffmpeg` (which you can invoke via `popen` or similar), extract frames from the video to detect the FIRST frame that is completely black (average RGB value of all pixels is 0). 
   - The service must listen for incoming TCP connections on port `8080`.
   - It should implement a basic HTTP/1.0 server. When it receives a `GET /anomaly` request with the header `Authorization: Bearer factory-edge-token-99`, it must respond with an HTTP 200 OK status and the body containing exactly the integer frame number of the first black frame.
   - For unauthorized requests or other paths, return standard HTTP 401 or 404 errors.
   - The C program must log every incoming request to `/home/user/logs/server.log`. The log format must be `[YYYY-MM-DD HH:MM:SS] <path> <status_code>\n`. 
   - CRITICAL: The application must force the timezone for its logs to be `Europe/Berlin` and use the `de_DE.UTF-8` locale for any date formatting, regardless of the system's default timezone.

3. **Process Supervision:**
   - Configure a `supervisord` setup to manage your compiled C binary (`/home/user/src/video_server`).
   - Create the configuration file at `/home/user/supervisor/supervisord.conf`. 
   - The supervisor must be configured to automatically restart the C binary if it crashes, and capture stderr to `/home/user/logs/server_err.log`.
   - Start the `supervisord` process in the background using this configuration.

4. **Log Rotation:**
   - Create a `logrotate` configuration file at `/home/user/logrotate.conf`.
   - It must rotate `/home/user/logs/server.log` daily, keep 5 backups, compress the old logs, and copy-truncate to avoid restarting the C service.

Compile your C program, start your supervisor, and leave the service running on port 8080.