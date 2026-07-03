You are acting as a FinOps engineer trying to recover lost cost-telemetry data and restore a centralized cost-dashboard service. A recent network misconfiguration severed communication between our cloud microservices. Before the network failed, a fallback telemetry system dumped the billing metrics into a video file where each frame contains a QR code with a JSON payload.

Your objective is to extract the billing data, calculate the total optimized cost, and deploy a robust, supervised dashboard service to serve this data.

Step 1: Telemetry Recovery
A video artifact is located at `/app/cloud_telemetry.mp4`. Use `ffmpeg` and Python (e.g., `pyzbar`, `Pillow`, or `opencv-python`) to extract and decode the QR codes from the video. 
Each QR code contains a JSON payload like: `{"service": "auth", "base_cost": 150, "idle_waste": 30}`.
Calculate the "optimized cost" for each service: `optimized_cost = base_cost - idle_waste`. 
Calculate the `total_optimized_cost` across all unique services found in the video.

Step 2: Dashboard Service
Write a Python web server (you may use Flask, FastAPI, or the standard library) that listens on `127.0.0.1:8080`.
It must expose the following HTTP GET endpoints:
- `/health`: Returns HTTP 200 with `{"status": "ok"}`
- `/costs`: Returns HTTP 200 with `{"total_optimized_cost": <FLOAT_VALUE>}` based on the data you extracted.
- `/crash`: Immediately terminates the web server process (e.g., via `os._exit(1)`) to simulate a fatal crash.

Step 3: Process Supervision & Logging
We cannot rely on systemd as you do not have root privileges. Write a Python supervisor script at `/home/user/supervisor.py` that:
1. Spawns the dashboard service as a subprocess.
2. Monitors the process. If it crashes (e.g., via the `/crash` endpoint), the supervisor must restart it within 3 seconds.
3. Captures all standard output and standard error from the dashboard service and writes it to `/home/user/logs/dashboard.log`.
4. Implements log rotation for `/home/user/logs/dashboard.log`. When the file reaches 10 KB (10240 bytes), it should be rotated (e.g., renamed to `dashboard.log.1`), keeping a maximum of 3 backup files (`dashboard.log.1`, `dashboard.log.2`, `dashboard.log.3`).

Start your supervisor script in the background so the dashboard service is running and resilient.

Constraints:
- You have access to python3 and pip. You can install any necessary user-space libraries.
- The `libzbar0` and `ffmpeg` system packages are already installed.
- Ensure the `/home/user/logs/` directory exists before starting your supervisor.