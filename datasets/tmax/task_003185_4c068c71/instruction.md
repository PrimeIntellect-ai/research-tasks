You are acting as a FinOps engineer. We have a lightweight internal cost-reporting service composed of Nginx and a Python Flask backend. The service recently broke during a server migration, and the dashboard is currently receiving 502 Bad Gateway errors. Your goal is to fix the service, configure it to dynamically discover its data volume, and implement a missing data processing endpoint.

Here is the current state of the system:
1. **Nginx** is configured to run on port 8080. Its configuration file is located at `/home/user/nginx/nginx.conf`. It is supposed to proxy requests to a backend Python service via a Unix socket, but the `proxy_pass` directive has an incorrect socket path. Nginx is currently running.
2. The **Python Backend** is located at `/home/user/app/api.py`. It is a Flask application that should be served using Gunicorn.
3. The server simulates mounted volumes for cost data. A custom fstab file exists at `/home/user/vfs/fstab`. 

Your tasks are to:

**Step 1: Fix the 502 Bad Gateway**
Identify the intended socket path in `/home/user/app/start.sh` (or choose your own, e.g., `/home/user/app/api.sock`). Fix `/home/user/nginx/nginx.conf` so the upstream points to this socket, and restart/reload Nginx. Start the Python backend using Gunicorn bound to this Unix socket.

**Step 2: Dynamic Volume Discovery**
The backend needs to read a billing log file, but the mount point changes. Modify `/home/user/app/api.py` to programmatically parse `/home/user/vfs/fstab`. Find the line where the filesystem type is `ext4` and the mount options include the string `finops=true`. Extract the mount point directory from this line. The billing log will be located at `<mount_point>/billing.log`.

**Step 3: Implement the `/metrics` Endpoint**
In `/home/user/app/api.py`, implement the `/metrics` HTTP GET endpoint. This endpoint must:
- Locate `billing.log` using the logic from Step 2.
- The `billing.log` file is a pipe-separated file (`|`) with columns: `timestamp|service_name|instance_id|cost`.
- Use a subprocess call to a text processing pipeline (e.g., `awk`) to calculate the total cost per `service_name`.
- Return a JSON response mapping service names to their total aggregated costs as floats. Example: `{"EC2": 150.50, "S3": 20.0}`.

Ensure your Python application is running as a daemon or background process so the port remains open, and verify that `curl http://127.0.0.1:8080/metrics` returns the correct JSON.