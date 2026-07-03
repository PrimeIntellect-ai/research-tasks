You are an engineer tasked with diagnosing and fixing a local Python-based data ingestion daemon that is failing to start. The daemon is managed by a local supervisor script, but it currently crash-loops on startup.

Your objectives:
1. **Connectivity Configuration:** The daemon connects to an upstream target, but the configuration file (`/home/user/app/config.json`) is missing the target IP and port. The original documentation is lost, but a screenshot of the old legacy dashboard has been recovered at `/app/config_snapshot.png`. You must extract the upstream IP address and port from this image and update `/home/user/app/config.json` accordingly.
2. **Application User Administration:** The daemon's internal authentication module strictly requires an application-level user named `svc_ingest` assigned to the `network_admins` group in the local credentials file located at `/home/user/app/auth.json`. You must create or update this user and group mapping appropriately in the JSON file.
3. **Startup Optimization:** The daemon's initialization routine (`startup_check()` in `/home/user/app/daemon.py`) processes a large list of mock historical telemetry hashes. Currently, it takes far too long (over 5 seconds), causing the local supervisor to kill it due to a startup timeout. You must analyze and rewrite the `startup_check()` function in `daemon.py` to be dramatically faster without changing its expected return value.
4. **Scheduled Diagnostics:** To ensure ongoing reliability once fixed, configure a scheduled task for the current user (`user`) using `cron`. The cron job must run the diagnostic script `/home/user/app/health_ping.py` exactly every 5 minutes.

Verification:
- The supervisor will evaluate if the daemon starts successfully.
- An automated benchmark will load your modified `daemon.py` and measure the execution time of `startup_check()`. It must execute in less than 0.5 seconds.
- The `cron` configuration for the user will be checked programmatically.