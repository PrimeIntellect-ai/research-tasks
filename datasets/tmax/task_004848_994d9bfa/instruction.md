You are an edge computing engineer configuring a localized telemetry gateway for IoT devices. 

We have a vendored telemetry daemon located at `/app/edge-telemetry`. This daemon receives HTTP health checks from edge nodes and TCP log streams from sensors. However, the current vendored package has a misconfiguration and fails to run properly. 

Your tasks are:

1. **Fix the Vendored Package**: 
   The service start script `/app/edge-telemetry/start.sh` has a deliberate typo in its environment variable assignment that prevents the Python server from binding to all interfaces (`0.0.0.0`). Find the typo in `start.sh` and fix it using standard shell tools (e.g., `sed`).

2. **Deploy the Service**:
   Ensure the directory `/home/user/logs` exists. 
   Start the service by executing the fixed `/app/edge-telemetry/start.sh`. The service must be running in the background and logging its output to `/home/user/logs/telemetry.log`.
   The service must successfully listen on:
   - HTTP Port: `8080` (Health checks)
   - TCP Port: `8081` (Raw sensor logs)

3. **Configure Log Rotation**:
   The edge device has limited storage. Create a logrotate configuration file at `/home/user/telemetry-logrotate.conf` that applies to `/home/user/logs/telemetry.log`. It must specify:
   - Daily rotation
   - Keep 7 days of backlogs (rotate 7)
   - Compress the rotated logs
   - Missing ok (`missingok`)
   - Do not rotate if empty (`notifempty`)

Write a robust Bash script at `/home/user/deploy.sh` that automates steps 1 and 2, and create the logrotate config. Ensure the daemon is actively running and listening on the specified ports before you finish.