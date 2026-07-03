You are a backup operator testing a newly restored batch of backend API servers. You need to ensure they can be managed, load-balanced, and are healthy before signing off on the restore operation.

The restored application files are located in `/home/user/restored_apps/`. There are three Python backend servers (`app1.py`, `app2.py`, `app3.py`) designed to run on ports 9001, 9002, and 9003 respectively.

Your task is to complete the following:

1. **Service Lifecycle Management:**
   Write a Bash script at `/home/user/manage_services.sh` that acts as an init script for these three apps. 
   - It must accept three arguments: `start`, `stop`, and `status`.
   - `start`: Starts `app1.py`, `app2.py`, and `app3.py` in the background. It must save their PIDs into `/home/user/run/app1.pid`, `/home/user/run/app2.pid`, and `/home/user/run/app3.pid`. (You will need to create the `/home/user/run` directory).
   - `stop`: Reads the PIDs from the PID files, terminates the processes, and removes the PID files.
   - `status`: Exits with code 0 if all three PID files exist and the processes are running, otherwise exits with code 1.
   Start the services using your script.

2. **Reverse Proxy and Health Checks:**
   Create an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - Bind a frontend to `127.0.0.1:8080`.
   - Set up a backend using the `roundrobin` balance algorithm pointing to the three apps on `127.0.0.1:9001`, `9002`, and `9003`.
   - Crucially, enable HTTP health checks for the backend servers (using the `check` option). The apps respond to `/ping`.
   - Start HAProxy in daemon mode: `haproxy -f /home/user/haproxy.cfg -p /home/user/run/haproxy.pid -D`.

3. **Diagnose and Fix the Restore:**
   One of the restored apps is failing to start properly or failing its health check due to a missing dummy database file that wasn't included in the restore archive.
   - Inspect the apps or use HAProxy/curl to determine which app is returning a 503 error.
   - Create the missing file `/home/user/restored_apps/db.sqlite` (it can be an empty file) to fix the app. Once the file exists, the app will automatically recover and return 200 OK.

4. **Verification Script:**
   Write a Bash script at `/home/user/verify_restore.sh` that performs the final validation.
   - It should use `curl` to make exactly 12 requests to `http://127.0.0.1:8080/ping`.
   - It must extract just the HTTP status code (e.g., `200`) for each request.
   - It must write these status codes, one per line, into `/home/user/proxy_results.log`.

To complete the task, ensure all services (the 3 apps and haproxy) are running, the missing file is created, and run your `verify_restore.sh` script to populate the log file.