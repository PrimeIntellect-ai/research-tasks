You are a container specialist responsible for modernizing a legacy video-analytics microservice. We have a surveillance video file located at `/app/data/surveillance.mp4`. Your task is to build a CI/CD-style pipeline that processes this video, compiles a C-based HTTP microservice, and serves the data securely via a reverse proxy.

Perform the following steps:

1. **Environment Setup & Processing Pipeline**:
   - Create a working directory at `/home/user/analytics/src`.
   - Use `ffprobe` to extract the presentation timestamps (`pts_time`) of every frame in the video stream of `/app/data/surveillance.mp4`.
   - Use text processing tools (`awk`, `sed`, or similar) to format these timestamps into a C header file located at `/home/user/analytics/src/timestamps.h`. The file must declare an array exactly like this:
     `const double frame_timestamps[] = { 0.000000, 0.033333, ... };`
     (Include all timestamps in sequential order).
   - Define a shell environment variable `PIPELINE_STRICT=1` in your `~/.bashrc` (or equivalent profile) to simulate our CI environment requirements.

2. **C Backend Implementation**:
   - Write a C program at `/home/user/analytics/src/backend.c` that acts as a simple HTTP server.
   - It must include the generated `timestamps.h`.
   - It must listen on TCP port `9000` on `127.0.0.1`.
   - When it receives an HTTP `GET` request exactly matching `/api/time?frame=<N>` (where `<N>` is an integer index starting from 0), it should respond with an HTTP 200 OK status and a JSON payload: `{"frame": <N>, "time": <TIMESTAMP>}`, replacing `<TIMESTAMP>` with the exact double value from the array.
   - If `<N>` is out of bounds, respond with an HTTP 404.
   - Compile this program into an executable named `/home/user/analytics/backend`.

3. **Web Server & TLS Configuration**:
   - Generate a self-signed TLS certificate and private key at `/home/user/analytics/certs/server.crt` and `/home/user/analytics/certs/server.key`.
   - Create a custom Nginx configuration file at `/home/user/analytics/nginx.conf`. Because you do not have root access, ensure that Nginx is configured to use `/tmp/nginx/` for its PID file, temp directories, and logs.
   - Configure Nginx to listen on HTTPS port `8443` on `127.0.0.1` using your self-signed certificate.
   - Nginx must act as a reverse proxy, forwarding all requests matching the location `/api/time` to your C backend listening on `127.0.0.1:9000`.

4. **Integration**:
   - Start the C backend executable in the background.
   - Start Nginx in the background using your custom configuration: `nginx -c /home/user/analytics/nginx.conf`.

Verify your setup by ensuring both `curl http://127.0.0.1:9000/api/time?frame=5` and `curl -k https://127.0.0.1:8443/api/time?frame=5` return the correct JSON structure.