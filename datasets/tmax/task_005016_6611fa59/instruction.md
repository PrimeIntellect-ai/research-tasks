You are tasked with building a configuration tracking service for our legacy hardware servers. Our automated data center monitoring system outputs two critical pieces of information:
1. A baseline configuration schedule in CSV format at `/home/user/baseline_config.csv`.
2. A raw video feed from the server rack's diagnostic display panel, located at `/app/rack_monitor.mp4`.

The diagnostic display in the video flashes brightly when a configuration anomaly or unlogged changepoint occurs. You must write a C++ program that processes this data and exposes an HTTP service to query the configuration state and anomalies.

Requirements for your C++ service:
1. **Video Streaming & Anomaly Detection**: Stream the video using an `ffmpeg` pipe directly into your C++ program (do not extract all frames to disk, as this mimics a continuous stream). Process the frames (assume 10 FPS, grayscale) and compute the average pixel intensity of each frame. An anomaly/changepoint occurs in any frame where the average pixel intensity is strictly greater than `128.0`.
2. **Merge & Join**: Read `/home/user/baseline_config.csv` (which contains `timestamp_sec,config_id`). Join the detected anomalies from the video stream with the baseline configuration. 
3. **Interpolation**: The CSV only lists config IDs at specific integer seconds. If an anomaly occurs at an unlisted fractional second, use nearest-neighbor interpolation to assign the `config_id` for that anomaly.
4. **Service**: Implement an HTTP service listening on `127.0.0.1:8080`.
   - Endpoint: `GET /anomalies`
   - Authorization: Must accept requests with the header `Authorization: Bearer trace-mgr-77`
   - Response: A JSON array of all detected anomalies in chronological order, e.g., `[{"time_sec": 1.2, "config_id": "cfg_alpha"}, ...]`. Time should be precise to 1 decimal place (since the video is exactly 10 FPS).

You may use standard Linux tools (like `ffmpeg`), build systems (`g++`, `cmake`), and any C++ libraries you wish to install (e.g., `cpp-httplib`, `nlohmann/json`) to complete this task. 

Start the service in the background and ensure it is listening on port 8080 before completing your turn.