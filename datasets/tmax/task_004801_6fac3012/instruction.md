You are an observability engineer tuning dashboards for filesystem monitoring. You need to deploy a new filesystem metrics parser written in C++ using a staged deployment approach.

Your task is to write a C++ program and a bash deployment script to process raw filesystem metrics into a human-readable log format for the dashboard backend.

1. Create a raw metrics file at `/home/user/raw_fs.txt` with exactly this single line of content:
`1672531200 /var/log 5048392`

2. Write a C++ program at `/home/user/agent.cpp` that does the following:
- Reads the filesystem metrics from `/home/user/raw_fs.txt` (format: `<unix_timestamp> <mount_point> <bytes_free>`).
- Reads the environment variable `METRICS_ENV`.
- Opens (or creates) `/home/user/observability.log` in append mode.
- Converts the Unix timestamp to a local time string formatted exactly as `YYYY/MM/DD HH:MM:SS` (using standard C++ time libraries which respect the `TZ` environment variable).
- Appends a single line to `/home/user/observability.log` in this exact format:
`[{FORMATTED_TIME}] Mount: {MOUNT_POINT} | Free: {BYTES_FREE} bytes | Env: {METRICS_ENV}`

3. Write a deployment script at `/home/user/deploy.sh` that performs these steps:
- **Connectivity Diagnostic:** Pings `127.0.0.1` exactly once. If successful, appends the exact string `Connectivity OK` to `/home/user/observability.log`.
- **Compilation:** Compiles `/home/user/agent.cpp` into an executable named `agent_bin`.
- **Staged Deployment:** Creates two directories: `/home/user/deploy_blue` and `/home/user/deploy_green`. Copies `agent_bin` into both directories.
- **Environment & Execution:** Sets the timezone environment variable `TZ` to `Asia/Tokyo`, sets `LC_ALL=C`, and sets `METRICS_ENV=tuning_stage`. While these variables are exported/active, executes the binary from the green environment: `/home/user/deploy_green/agent_bin`.

Make sure to make the script executable and run `/home/user/deploy.sh` so the final log file is generated.