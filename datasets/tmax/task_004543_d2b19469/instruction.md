You are a monitoring specialist tasked with setting up an automated video-based alert system for a legacy server room that lacks direct telemetry. We have a camera feed recording the status LED of a critical server, provided as a video file.

Your tasks:
1. **Video Analysis (Python):** 
   Write a Python script `/home/user/monitor.py` that processes the video at `/app/rack_monitor.mp4`. The video is encoded at 30 FPS. You must detect "Alert States". An Alert State occurs when the status LED turns red. Specifically, detect frames where the average Red channel value across the entire frame is greater than 150, and both Green and Blue channels average less than 50. 
   For every frame that meets this condition, the script must append a line to `/home/user/alerts.log` in exactly this format:
   `ALERT: Frame <N>` (where `<N>` is the 0-indexed frame number).

2. **Connectivity & Alerting:**
   There is a local alert aggregator running on this machine, but its port is undocumented and changes on startup. You must use standard diagnostic tools (like `ss`, `netstat`, or `lsof`) to find the local TCP port it is listening on. It is a simple HTTP server. Modify your `monitor.py` script so that, for each alert frame detected, it also sends an HTTP POST request to `http://127.0.0.1:<PORT>/alert` with a JSON payload: `{"frame": N}`.

3. **Process Supervision:**
   The `monitor.py` script occasionally crashes due to simulated memory leaks. Create a bash script `/home/user/watchdog.sh` that acts as a process supervisor. It should execute `monitor.py` and, if `monitor.py` exits with a non-zero exit code, automatically restart it. The watchdog should run continuously until `monitor.py` exits successfully (exit code 0).

4. **Permissions Management:**
   Security policy requires that the alert logs are heavily restricted. Ensure that `/home/user/alerts.log` is created with or modified to have `600` permissions (read/write for the owner only, no permissions for group or others).

Ensure you leave the final `/home/user/alerts.log` fully populated by running your watchdog script.