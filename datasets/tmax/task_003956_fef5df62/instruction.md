You are an observability engineer tasked with tuning dashboards, which requires custom metrics from a legacy application. The application writes basic access logs, but you need an automated, reliable pipeline to extract status code metrics, aggregate them, and expose them as a JSON file.

Your goal is to write a Go program to aggregate these metrics, and an idempotent bash script to deploy this tool as a scheduled systemd user service.

**Phase 1: The Go Metrics Exporter**
Write a Go program at `/home/user/src/exporter.go` that:
1. Reads `/home/user/data/requests.log`. Each line is formatted as: `TIMESTAMP STATUS_CODE PATH` (e.g., `1690000000 200 /api/v1/data`).
2. Calculates the total count for each HTTP status code present in the file.
3. Outputs the aggregated counts as a formatted JSON object to `/home/user/metrics/summary.json`. 
   Example output:
   `{"200": 45, "404": 2, "500": 1}`
4. If `/home/user/metrics/summary.json` exists, it should be overwritten.

**Phase 2: The Idempotent Deployment Script**
Write a bash script at `/home/user/deploy.sh` that performs the following steps idempotently (running it multiple times must be safe and result in the exact same final system state):

1. **Compilation:** Compiles `/home/user/src/exporter.go` and places the executable at `/home/user/bin/exporter`. (Create the directory if it does not exist).
2. **Directory Management:** Creates `/home/user/metrics` if it doesn't exist.
3. **Permissions:** Modifies the permissions of `/home/user/metrics` so that only the owner has read, write, and execute permissions (no permissions for group or others).
4. **Service Configuration:** Creates a systemd user service unit file at `/home/user/.config/systemd/user/exporter.service` (create the directory path if needed). 
   - The service description must be `"Custom Metrics Exporter"`.
   - The `ExecStart` must point to `/home/user/bin/exporter`.
   - The `Type` must be `oneshot`.
5. **Timer Configuration:** Creates a systemd user timer unit file at `/home/user/.config/systemd/user/exporter.timer`.
   - The timer description must be `"Run Exporter Every Minute"`.
   - It must run `OnCalendar=*-*-* *:*:00` (every minute).
6. **Service Lifecycle:** Enables and starts the `exporter.timer` using `systemctl --user`. 

**Execution:**
Once you have written `exporter.go` and `deploy.sh`, make `deploy.sh` executable and run it. Verify that the compilation succeeds, the systemd unit files are accurately created, the directories have the correct permissions, and that executing `/home/user/bin/exporter` manually correctly generates the `/home/user/metrics/summary.json` file.