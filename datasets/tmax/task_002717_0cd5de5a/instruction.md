You are a deployment engineer tasked with finalizing a secure reverse-proxy setup for a new Python backend service. 

Currently, our application environment is partially configured in `/app`. We are using a multi-service architecture consisting of:
1. An Nginx reverse proxy (listening on port 8080).
2. A Python backend API (listening on port 9090).
3. A local SSH daemon running as the non-root user (listening on port 2222).

Your goal is to securely route traffic from Nginx to the Python API over an SSH tunnel, fix an authentication issue, and ensure the backend logs are properly rotated.

**Part 1: Fix SSH Authentication**
The local SSH daemon is configured via `/app/ssh/sshd_config`. Currently, it silently rejects the provided deployment key (`/app/ssh/deploy_key`).
- Diagnose and fix the configuration in `/app/ssh/sshd_config` so that key-based authentication works for the user `user` using the provided `deploy_key`.
- Restart the SSH daemon. (You can manage services using the provided `/app/scripts/manage_services.sh restart sshd` command).

**Part 2: Establish the SSH Tunnel**
Once SSH is fixed, establish a persistent background SSH tunnel.
- Use the deployment key (`/app/ssh/deploy_key`).
- Forward local port `8081` to the backend API at `127.0.0.1:9090` through the SSH server on port `2222`.
- Ensure the tunnel runs in the background and does not require an interactive terminal.

**Part 3: Configure Nginx**
Nginx is serving as our front-end entry point.
- Edit the Nginx configuration file at `/app/nginx/nginx.conf`.
- Configure it so that any HTTP requests coming to `127.0.0.1:8080` are proxied to your newly created SSH tunnel at `127.0.0.1:8081`.
- Restart Nginx using `/app/scripts/manage_services.sh restart nginx`.

**Part 4: Log Configuration and Rotation**
The Python backend writes its request logs to `/app/logs/backend.log`. We need to ensure these logs do not fill up the disk.
- Create a local logrotate configuration file at `/app/logrotate.conf`.
- Configure it to rotate `/app/logs/backend.log` when it reaches a size of `100k`.
- Keep exactly `3` compressed backups (using gzip).
- Do not use `su` directives (as you are running as a non-root user). 
- Run logrotate manually using `logrotate -s /app/logs/logrotate.status /app/logrotate.conf` to verify the syntax is correct. (You do not need to set up a cron job for this task, just the config file and status file).

**Part 5: Benchmark and Verification**
Once everything is running, you must run the load test script located at `/app/scripts/benchmark.sh`.
This script will send 500 requests to Nginx on port 8080. If your tunnel and proxy are configured correctly, Nginx will pass these to port 8081, through the SSH tunnel, to the Python backend on port 9090.
- Execute `/app/scripts/benchmark.sh > /app/benchmark_results.json`.
- The benchmark tool will output a JSON payload containing the metric `success_rate`.
- To pass this task, your `success_rate` must be greater than or equal to `0.95`.

**Environment Details:**
- All work must be done within `/app`.
- The SSH daemon host keys and authorized_keys are pre-staged in `/app/ssh/`.
- Do not attempt to use `sudo` or modify system-wide files outside of `/app`.