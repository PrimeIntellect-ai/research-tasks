You are acting as a system engineer diagnosing a network service that fails to start. 

A custom Go-based network service is located at `/home/user/service/daemon.go`. It reads configuration from `/home/user/service/config.json`, requires specific locale and timezone configurations to interact with its upstream Japanese API, and has an interactive security prompt on startup. Currently, it crashes or fails to start.

Your task is to diagnose the issues and automate the startup process. Complete the following objectives:

1. **Analyze and Fix Configuration:** 
   Read `/home/user/service/daemon.go`. It reads `/home/user/service/config.json`. The current `config.json` is corrupted/incorrect. Fix it so the service binds to port `8080`.

2. **Automate Startup with Expect:**
   Write an expect script at `/home/user/start_service.exp`. This script must:
   - Set the required Timezone (`TZ`) and Locale (`LANG`) environment variables as expected by the Go daemon's source code.
   - Run the Go service (`go run /home/user/service/daemon.go`).
   - Automatically answer the interactive PIN prompt by extracting the correct PIN from the Go source code logic.
   - Wait for the service to finish (it will write to its log and exit gracefully after 2 seconds if successful).

3. **Configure Log Rotation:**
   The service outputs logs to `/home/user/service/daemon.log`. Create a logrotate configuration file at `/home/user/logrotate.conf` that manages this specific log file. It must:
   - Rotate the log `daily`.
   - Keep exactly `3` rotations (`rotate 3`).
   - Create new log files after rotation.

Ensure you execute your `/home/user/start_service.exp` script successfully so that `/home/user/service/daemon.log` is generated and contains the successful startup message.