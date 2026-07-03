You are acting as a network engineer setting up a connectivity monitoring tool. 

Please perform the following tasks in the `/home/user` directory:

1. **Directory and Link Management:** 
   Create a directory named `/home/user/network_tools`.
   Create an executable Python script inside it named `/home/user/network_tools/check_conn.py`.
   Create a symbolic link at `/home/user/active_tool` that points to `/home/user/network_tools/check_conn.py`.

2. **Python Script (Timezone & Monitoring):**
   Write the script `check_conn.py` using Python. The script must do the following:
   - Make an HTTP GET request to `http://127.0.0.1:8080`.
   - Catch any connection errors or timeouts.
   - Append a single log line to `/home/user/conn.log` for each execution.
   - The log line must start with the current time in the `Asia/Tokyo` timezone, strictly formatted as `[YYYY-MM-DD HH:MM:SS JST]`.
   - If the HTTP request returns a 200 status code, append ` OK` to the line.
   - If the request fails, times out, or returns any other status code, append ` FAIL` to the line.
   - Example successful log line: `[2023-10-25 14:30:00 JST] OK`

3. **Scheduling:**
   Install a user crontab that executes `/home/user/active_tool` exactly every 5 minutes. Do not include any other cron jobs. 

Ensure the Python script has the correct execute permissions. You do not need to start an HTTP server on port 8080; the script should just gracefully handle the failure and log `FAIL` when the server is down.