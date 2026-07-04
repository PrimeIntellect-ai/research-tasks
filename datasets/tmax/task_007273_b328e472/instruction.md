You are a deployment engineer tasked with fixing a botched rollout of a custom disk monitoring agent. The previous engineer set up the monitoring script to run as a scheduled job, but because scheduled jobs (like cron) run in a restricted environment, the environment variables were missing. As a result, the script has been writing logs to a temporary fallback directory instead of the persistent storage volume, and the network metrics fail to send.

Your objective is to write the deployment scripts, fix the Python monitoring script, configure the environment, and establish a required network port forward. 

Please perform the following steps:

1. **Environment Setup:**
   Create an environment file at `/home/user/deploy/settings.env`. It must contain the following exported variables:
   - `METRICS_OUT_DIR=/home/user/app_data/metrics`
   - `METRICS_PORT=8888`

2. **Python Monitoring Script:**
   Create a Python script at `/home/user/deploy/disk_monitor.py`. This script must:
   - Read the `METRICS_OUT_DIR` environment variable. If it is not set, default to `/tmp/fallback_metrics`.
   - Ensure the output directory exists (create it idempotently).
   - Check the disk usage of the `/home/user` directory.
   - Write a file named `report.json` inside the output directory. The file must contain exactly this JSON payload: `{"status": "DISK_OK", "directory": "<the_actual_output_directory_path_used>"}`.
   - Read the `METRICS_PORT` environment variable. Make an HTTP GET request to `http://127.0.0.1:<METRICS_PORT>/ping` to signal that the script ran. Set a timeout of 3 seconds and safely catch any connection exceptions (do not crash if the port is unreachable).

3. **Job Wrapper Script:**
   Scheduled jobs run with a virtually empty environment. Create a bash script at `/home/user/deploy/job_wrapper.sh` that bridges this gap.
   - The script must source the `/home/user/deploy/settings.env` file.
   - It must then execute the `/home/user/deploy/disk_monitor.py` script using `python3`.
   - Ensure `job_wrapper.sh` has executable permissions.

4. **Port Forwarding (Network Configuration):**
   The metrics backend is actually listening on port `9999`, but the script is configured to talk to `8888`. 
   Set up a persistent port forward in the background that listens on `127.0.0.1:8888` and forwards all TCP traffic to `127.0.0.1:9999`. You can use `socat` or a background Python script to achieve this. Leave this running in the background.

To verify your work, we will simulate the cron environment by running your wrapper script with a completely empty environment:
`env -i /bin/bash /home/user/deploy/job_wrapper.sh`

Ensure all files are created exactly at the specified paths.