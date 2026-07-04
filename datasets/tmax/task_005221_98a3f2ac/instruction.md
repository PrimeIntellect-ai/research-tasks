You are a monitoring specialist tasked with building an automated video alert system. An edge device is recording a video feed and saving it to `/app/feed.mp4`. You need to build a lightweight Python-based microservice that analyzes this video, detects anomalous "blackout" frames, and exposes the findings via an HTTP API.

You must implement the following components without root privileges:

1. **The Analysis & Alerting Service (`/home/user/monitor.py`):**
   - Write a Python script that runs an HTTP server on `127.0.0.1:8080`.
   - On startup, the service should analyze `/app/feed.mp4`. The video runs at 1 frame per second.
   - An anomaly is defined as a frame that is completely black (average brightness of 0).
   - The service must expose two endpoints:
     - `GET /health` : Must return a 200 OK with JSON `{"status": "ok"}`.
     - `GET /alerts` : Must return a 200 OK with JSON `{"black_frames": [list_of_0_indexed_frame_numbers]}`.

2. **Service Lifecycle Management (`/home/user/manage.sh`):**
   - Write a sysvinit-style bash script to manage your Python service.
   - It must accept three commands: `start`, `stop`, and `status`.
   - `start`: Launches `monitor.py` in the background, writes its PID to `/home/user/monitor.pid`, and redirects output to `/home/user/monitor.log`.
   - `stop`: Reads the PID from `/home/user/monitor.pid`, terminates the process gracefully, and removes the PID file.
   - `status`: Exits with 0 if the process is running, or 1 if it is not.

3. **CI/CD Pipeline Simulation (`/home/user/deploy.sh`):**
   - Write a deployment script that orchestrates the setup.
   - The script should ensure any necessary python packages are installed (e.g., locally in `~/.local` or a venv if needed).
   - It should then use `./manage.sh stop` (ignoring errors if it wasn't running) followed by `./manage.sh start`.
   - Finally, it should poll the `http://127.0.0.1:8080/health` endpoint up to 10 times (with 1-second sleeps) until it gets a successful response, exiting 0 on success or 1 on timeout.

To complete the task, execute your `deploy.sh` script to ensure the service is running and properly initialized. Leave the service running when you finish.