You are tasked with automating the deployment and monitoring of a legacy, interactive service.

The legacy service is located at `/home/user/legacy_app/start_service.sh`. It is an interactive Bash script that prompts the user for configuration details before generating a configuration file and starting a background process.

You need to accomplish the following:

1. **Interactive Automation**: Write an `expect` script named `/home/user/automate.exp` that runs `/home/user/legacy_app/start_service.sh` and automatically answers its prompts:
   - Prompt: `Enter Environment (dev/prod):` -> Answer: `prod`
   - Prompt: `Enter Service Port [1000-9999]:` -> Answer: `8181`
   - Prompt: `Enable verbose logging? (y/n):` -> Answer: `y`
   Wait for the script to finish executing entirely.

2. **Idempotent Deployment**: Write a Bash wrapper script named `/home/user/deploy.sh`. This script must be idempotent.
   - It should check if the service is already deployed by verifying the existence of `/home/user/legacy_app/service.conf`.
   - If the configuration file exists, it should simply output "Deployment already configured." and exit with status code 0.
   - If it does not exist, it should execute `/home/user/automate.exp` to configure and start the service.
   - Ensure you run `/home/user/deploy.sh` at least once so the service is actually started.

3. **Health Check Monitoring**: The legacy service starts an HTTP server on the port you configured. Write a Bash script named `/home/user/health_monitor.sh` that uses `curl` to send a GET request to `http://127.0.0.1:8181/health`.
   - If the HTTP response body is exactly `OK`, the script must append the exact line `STATUS: HEALTHY` to `/home/user/health_report.log`.
   - If the response is anything else, or if the connection fails, it must append `STATUS: UNHEALTHY` to `/home/user/health_report.log`.
   - Run your `/home/user/health_monitor.sh` script exactly once to generate the initial log entry.

Ensure all scripts you create are executable. Do not use root/sudo, as you only have standard user permissions.