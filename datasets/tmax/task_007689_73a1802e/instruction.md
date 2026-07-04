You are an edge computing engineer configuring the deployment stage for a fleet of IoT devices. You need to create an idempotent configuration script in Python that mimics a CI/CD deployment step. This script will generate the local reverse proxy configuration, log rotation policies, and a deployment manifest for the device.

Write a Python script at `/home/user/deploy_edge.py` that fulfills the following requirements:

1. **CLI Arguments**: The script must accept a `--backends` argument, which takes a comma-separated list of port numbers (e.g., `--backends 9001,9002`).
2. **Idempotency**: The script must be fully idempotent. Running it multiple times with the same arguments must result in the exact same system state, without duplicating configuration lines or failing.
3. **Target Directory**: The script must create and operate within `/home/user/iot_env/`. 
4. **Reverse Proxy Configuration**: The script must generate a valid Nginx configuration file at `/home/user/iot_env/nginx.conf`. The config must contain:
    - An `upstream backend_cluster` block that includes a `server 127.0.0.1:<port>;` line for each port provided in the `--backends` argument.
    - A `server` block that listens on port `8080`.
    - A `location /` block that uses `proxy_pass http://backend_cluster;`.
    - An access log directive writing to `/home/user/iot_env/access.log`.
5. **Log Rotation**: The script must generate a logrotate configuration file at `/home/user/iot_env/logrotate.conf` specifically for `/home/user/iot_env/access.log`. It must contain exactly the following directives for the file: `daily`, `rotate 7`, `compress`, `missingok`, and `notifempty`.
6. **CI/CD Manifest**: The script must generate a JSON file at `/home/user/iot_env/manifest.json` indicating the success of the deployment pipeline. It should have the exact structure:
    ```json
    {
      "deployed_backends": [9001, 9002],
      "status": "success"
    }
    ```
    *(Note: The array must contain integers, matching the inputs from the `--backends` argument).*

Ensure your Python script uses standard libraries only (e.g., `os`, `sys`, `json`, `argparse`). You do not need to start Nginx or logrotate; you only need to reliably generate the correct configuration files.