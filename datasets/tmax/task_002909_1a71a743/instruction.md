You are an observability engineer tasked with fixing a broken custom logging pipeline and extracting metrics for a dashboard. The logging architecture relies on an application writing to a local Unix socket, which a log aggregator daemon reads from. The pipeline is currently failing, and the aggregator daemon's supervisor is misconfigured.

Please complete the following tasks to restore the system and generate the required metrics. All files are located within `/home/user/`.

**1. Configuration Backup**
Before making any changes, back up the existing configuration. 
Create a compressed tarball of the `/home/user/config` directory and save it as `/home/user/backups/config_backup.tar.gz`.

**2. Fix the Upstream Socket Configuration**
The application is currently throwing "502 Bad Gateway" errors because it is trying to send logs to the wrong socket path. 
Edit `/home/user/config/app.conf`. You will notice the `upstream_socket` variable has a typo. Change it so that it correctly points to `/home/user/run/aggregator.sock`.

**3. Fix Process Supervision**
The log aggregator is supervised by a custom shell script: `/home/user/supervisor.sh`. Currently, if the aggregator crashes, the supervisor restarts it immediately in an infinite tight loop, causing CPU spikes.
Modify `/home/user/supervisor.sh` to introduce a 5-second delay (`sleep 5`) immediately before the daemon is restarted inside the `while` loop.

**4. Generate Dashboard Metrics via Text Processing**
Because of the socket issue, the application has generated numerous errors in `/home/user/logs/error.log`. 
You need to extract the counts of "Connection refused" errors grouped by the minute they occurred.
Parse `/home/user/logs/error.log` and generate a summary file at `/home/user/dashboard_metrics.txt`.
The output file must contain exactly one line per minute that had errors, sorted chronologically, in the following format:
`[YYYY-MM-DD HH:MM] - <COUNT> errors`

Example of the expected format in `/home/user/dashboard_metrics.txt`:
`[2023-10-25 14:01] - 3 errors`
`[2023-10-25 14:02] - 5 errors`

Ensure all these steps are completed using standard command-line tools.