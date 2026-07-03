You are an engineer stepping into a deployment issue. A previous engineer attempted to deploy a proprietary, stripped telemetry daemon located at `/app/telemetry_gateway`, but the automated deployment script they wrote is failing to start the service properly in our production-like environment. 

The previous engineer left a broken wrapper script at `/home/user/start_service.sh`. When run, the service immediately crashes or fails to bind. It is suspected that the issue involves missing environment variables and a stripped environment (similar to how `cron` strips the `PATH` variable, preventing system utilities from being found).

Your objectives:
1. **Analyze the Binary:** Reverse engineer or trace the stripped binary `/app/telemetry_gateway` to determine what environment variables it requires to run successfully.
2. **Fix the Environment & Wrapper:** Update `/home/user/start_service.sh` (using Bash) to provide the correct environment. You must:
    * Set the port environment variable so the daemon binds exactly to `127.0.0.1:8443`.
    * Set the authentication token variable to `admin-secret-991`.
    * Set the data directory variable to `/home/user/gateway_data` (create this directory).
    * Fix the `PATH` or related environment issues so the binary can successfully execute any system utilities it relies on internally (e.g., `curl` or `nc`).
3. **Launch the Service:** Run your fixed `/home/user/start_service.sh` in the background so the daemon remains running on port 8443.
4. **Health Check Script:** Write an automated Bash health check script at `/home/user/health_check.sh` that queries the daemon's HTTP `/status` endpoint on port 8443, passing the required authentication token. The script should exit 0 if the daemon responds successfully, and exit 1 otherwise.

Leave the `telemetry_gateway` process running in the background when you are finished. The automated verification system will test both the binary's running state and its network responses.