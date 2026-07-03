You are tasked with deploying a custom Go-based storage monitoring service and writing a diagnostic script to verify its connectivity and functionality. 

Perform the following steps exactly as described:

1. **Environment Setup:**
   - Create a directory structure: `/home/user/workspace/disk_monitor/`, `/home/user/workspace/data/`, and `/home/user/workspace/config/`.
   - Inside `/home/user/workspace/data/`, create a dummy file named `dummy.dat` exactly 5 Megabytes (5,242,880 bytes) in size.

2. **System Configuration:**
   - Create a JSON configuration file at `/home/user/workspace/config/settings.json`.
   - The JSON file must contain exactly two keys:
     - `"monitor_dir"`: set to the string `"/home/user/workspace/data"`
     - `"quota_mb"`: set to the integer `15`

3. **Go Application (Storage Monitor):**
   - Write a Go application inside `/home/user/workspace/disk_monitor/main.go`.
   - The application must read the `/home/user/workspace/config/settings.json` file.
   - It should calculate the total size (in Megabytes, rounded down to the nearest integer) of all files in the `monitor_dir`.
   - It must start an HTTP server listening on `127.0.0.1:8080`.
   - When a `GET` request is made to `/status`, it must return a JSON response with the HTTP status 200. The JSON response must have this exact structure:
     `{"status":"ok","usage_mb":<calculated_MB>,"quota_mb":<quota_from_config>}`
   - Initialize the go module (`go mod init monitor`) and compile the application to a binary named `monitor_service`.
   - Run the binary in the background so it continues to listen on port 8080.

4. **Connectivity Diagnostics:**
   - Write a bash script at `/home/user/workspace/check_conn.sh`.
   - The script must perform a connectivity check to see if port `8080` is listening on `127.0.0.1`.
   - If the port is listening, it should use `curl` to fetch the `/status` endpoint.
   - The script must write the raw JSON response body strictly to a log file located at `/home/user/workspace/monitor_results.log`.
   - Make the script executable and run it once to populate the log file.

Ensure all file paths and JSON keys are exactly as specified. The background service must remain running upon task completion.