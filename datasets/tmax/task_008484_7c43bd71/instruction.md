You are a capacity planner analyzing resource usage for a multi-language microservice architecture. The core metrics service is bound locally to port 9090, but your standard collection tooling is hardcoded to poll port 8080. 

Your task is to write an idempotent deployment script at `/home/user/setup_collector.sh` that automates the networking and scheduling setup for this collection.

The script must perform the following actions:
1. **Port Forwarding:** Start a background process using `socat` to forward traffic from `127.0.0.1:8080` (listen) to `127.0.0.1:9090` (destination). You must ensure this step is idempotent: if the script is run multiple times, it should not spawn duplicate `socat` processes or fail if the port is already bound by your forwarder.
2. **Connectivity Diagnostics:** After initiating the forwarder, the script must actively check and wait (with a timeout of up to 10 seconds) until `127.0.0.1:8080` is accepting connections before proceeding.
3. **Scheduled Task Configuration:** Add a cron job for the current user that executes `/home/user/record_capacity.sh` every minute (`* * * * *`). This step must also be strictly idempotent; running your setup script multiple times must result in exactly one instance of this cron job in the user's crontab.

Do not create the `/home/user/record_capacity.sh` script or the service on port 9090; assume they have already been deployed. Your script must be written in Bash and use standard Linux utilities. Ensure the script has executable permissions.