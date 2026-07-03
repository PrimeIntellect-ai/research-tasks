You are tasked with fixing a broken video analytics service. Currently, the local Nginx instance serving the API returns a `502 Bad Gateway`. The backend service is a C++ application that processes video files, creates a backup archive of the extracted frames, and serves the results. 

Your objectives are to fix the C++ application, correct the Nginx configuration, implement a process supervisor, and successfully extract data from a provided video file.

Here are the details of the system and what you must accomplish:

1. **Nginx Configuration:**
   - The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. Nginx is configured to listen on `127.0.0.1:8080`.
   - Nginx is attempting to proxy requests to the backend C++ service, but the proxy configuration has errors. Fix `/home/user/nginx/nginx.conf` so that all requests to `http://127.0.0.1:8080/` are correctly proxied to the backend HTTP service on `127.0.0.1:9000`.
   - Start Nginx using this local configuration (e.g., `nginx -c /home/user/nginx/nginx.conf`).

2. **C++ Backend Service:**
   - The source code is located at `/home/user/src/backend.cpp`. It uses the header-only library `httplib.h` (provided in `/home/user/src/`).
   - The application has several bugs preventing it from compiling, binding to the correct ports, and running successfully.
   - You must fix the code so that it:
     - Listens for HTTP requests on `127.0.0.1:9000`.
     - Listens for raw TCP status checks on `127.0.0.1:9001`. When a TCP client connects and sends the string `STATUS\n`, it must respond with `OK\n` and close the connection.
     - Implements an HTTP `GET /process` endpoint.

3. **Video Processing & Backup:**
   - When the `GET /process` endpoint is called, the C++ application must process the video file located at `/app/surveillance.mp4`.
   - It should use `ffmpeg` (which is pre-installed) to extract the frames from the video at 1 frame per second.
   - The application must analyze these frames to count exactly how many of the extracted frames are completely solid red (where all pixels have the exact RGB value of 255, 0, 0 or the dominant color is pure red).
   - The frames must then be archived into a tarball at `/home/user/backup/frames.tar.gz`. If the directory does not exist, the application must create it.
   - The HTTP response for `GET /process` must be `200 OK` with the `Content-Type: application/json` and a body formatted exactly as: `{"red_frames": <COUNT>}`.

4. **Process Supervision:**
   - Create a bash script at `/home/user/supervisor.sh` that continuously runs the compiled C++ application. If the C++ application crashes or exits, the supervisor must immediately restart it.
   - Start this supervisor script in the background.

Please complete all fixes and ensure Nginx, the supervisor, and the backend service are running in their final state.