You are an edge computing engineer deploying a lightweight video analysis and health-monitoring service to our IoT field devices. 

Your objective is to create a C-based microservice that analyzes a local video feed, monitors basic system health, respects specific locale/timezone constraints, and serves the results over HTTP.

Requirements:
1. **Timezone and Locale Setup:**
   The edge devices operate in Japan. Before your service runs, you must ensure it executes in the `Asia/Tokyo` timezone and the `ja_JP.UTF-8` locale for time formatting.

2. **Video Processing (C implementation):**
   Write a C program at `/home/user/edge_daemon.c` and compile it to `/home/user/edge_daemon`. 
   This program must analyze the video file located at `/app/edge_feed.mp4`.
   The C program should invoke `ffmpeg` (which is pre-installed) to extract frames from the video and count the exact number of completely black frames (where all RGB values are 0). 

3. **HTTP Service:**
   The C program must run as a daemon (or a continuous foreground process) listening on TCP port `8080`.
   It must respond to two HTTP GET requests:
   - `GET /health`: Returns a plain text `200 OK` response with the current system time formatted locally according to the `ja_JP.UTF-8` locale and `Asia/Tokyo` timezone (using `%c` formatting in `strftime`).
   - `GET /metrics`: Returns a plain text `200 OK` response containing exactly the text: `black_frames: <COUNT>` where `<COUNT>` is the integer number of completely black frames found in `/app/edge_feed.mp4`.

4. **Deployment Script:**
   Create a bash script at `/home/user/deploy.sh` that compiles the C program, sets the appropriate environment variables for the timezone and locale, and starts the `edge_daemon` process in the background.

Ensure your `edge_daemon` is robust enough to handle basic HTTP GET requests and uses standard POSIX sockets. Do not use heavy external web frameworks; standard C libraries are required.