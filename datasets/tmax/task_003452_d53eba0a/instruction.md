You are a deployment engineer tasked with rolling out an update for an internal backend service. The new version (V2) has just been staged, but the deployment rollout is currently failing. 

There are three main objectives to successfully complete this rollout:

1. **Fix the Proxy Health Check (502 Bad Gateway simulation):**
   The proxy's health check script at `/home/user/proxy/health_check.sh` is failing because it cannot connect to the backend's upstream socket. The configuration for the proxy is located at `/home/user/proxy/config.env`. Investigate where the backend service (`/home/user/backend/server.sh`) creates its Unix socket, and update `/home/user/proxy/config.env` to point to the correct path so the health check passes.

2. **Implement Storage Monitoring:**
   The V2 backend has a known bug where it writes excessively large, verbose logs to `/home/user/logs/backend.log`. If left unchecked, this will exhaust the disk quota and crash the process.
   Write a Bash script at `/home/user/storage_monitor.sh` that does the following in an infinite loop (sleeping for 2 seconds between iterations):
   - Checks the size of `/home/user/logs/backend.log`.
   - If the file exceeds 50000 bytes (50KB), empty the file (truncate it to 0 bytes) without deleting it or disrupting the backend process.

3. **Create and Run the Deployment Script:**
   Write a Bash script at `/home/user/deploy.sh` that orchestrates the deployment:
   - Starts the backend service (`/home/user/backend/server.sh`) in the background.
   - Starts your `storage_monitor.sh` in the background.
   - Sleeps for 5 seconds to allow the service and monitor to initialize.
   - Executes `/home/user/proxy/health_check.sh` and redirects the output strictly to `/home/user/deployment_result.log`.

Once you have written `storage_monitor.sh` and `deploy.sh` (make sure they are executable), and fixed the configuration, run `/home/user/deploy.sh`. Leave the background processes running so the testing suite can verify the final state.

Ensure `/home/user/deployment_result.log` contains a successful health check message.