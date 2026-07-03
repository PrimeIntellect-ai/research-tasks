You are an edge computing engineer deploying a new software stack to our IoT gateway devices. The current deployment is partially broken and needs to be finalized.

Complete the following tasks:

1. **Reverse Proxy Configuration:**
   We run a local Nginx instance as a reverse proxy. Its configuration file is located at `/home/user/edge_proxy/nginx.conf`. Currently, requests to the proxy return a 502 Bad Gateway error because the `upstream` socket path is incorrectly configured to `unix:/tmp/backend.sock`. Our data ingestion service actually listens on `unix:/home/user/run/app.sock`. Modify the Nginx configuration file to point to the correct upstream socket.

2. **Log Configuration & Rotation:**
   The Nginx instance writes logs to `/home/user/edge_proxy/logs/access.log` and `/home/user/edge_proxy/logs/error.log`. Create a logrotate configuration file at `/home/user/logrotate.conf` that applies to both of these log files. The configuration must:
   - Rotate logs daily.
   - Keep exactly 7 days of history (7 rotations).
   - Compress old log files.
   - Do not output errors if the log files are missing.

3. **Scheduled Task Configuration:**
   We have a monitoring script located at `/home/user/monitor.sh` (you do not need to create this script). Add an entry to the current user's crontab so that this script is executed exactly every 5 minutes.

4. **Sensor Data Encoder Replacement:**
   Our system relies on a legacy proprietary sensor encoder binary located at `/app/legacy_encoder`. Because we are migrating to a new architecture, we need to replace this black-box binary with a native C++ implementation.
   - The binary reads a single line from standard input containing exactly 4 space-separated integers: Temperature, Humidity, Pressure, and Light (each guaranteed to be between 0 and 10000).
   - It outputs a small binary payload to standard output based on these values.
   - Reverse engineer the behavior of `/app/legacy_encoder`. You can execute it and inspect its inputs and outputs to determine the binary format it produces.
   - Write a C++ program in `/home/user/encoder.cpp` that implements the exact same logic.
   - Compile your program to `/home/user/encoder`. Your executable must produce output that is bit-for-bit identical to `/app/legacy_encoder` for any valid input.

Ensure all paths and configurations exactly match the requirements.