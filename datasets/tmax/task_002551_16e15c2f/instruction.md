You are an observability engineer tasked with tuning our dashboards and restoring a broken telemetry pipeline. A critical incident was reported in an audio voicemail, but the original engineer is unreachable.

First, transcribe the voicemail located at `/app/incident_voicemail.wav`. (A tool like `whisper-cli` or similar is available in your environment). The voicemail contains:
1. Three critical IP addresses we need to monitor.
2. An error threshold percentage.

Second, the raw logs from the affected service are being served on a restricted local port (9090). To access them, you must establish an SSH tunnel. A custom SSH daemon is running locally on port 2222 under your user account (`user`). However, the local SSH configuration was recently corrupted and silently rejects key-based login.
- Diagnose and fix the permission/ACL issues in `/home/user/.ssh/` so that you can SSH to `127.0.0.1` on port `2222` using your key (`/home/user/.ssh/id_rsa`) without a password.
- Set up local port forwarding so that your local port `8080` forwards to `127.0.0.1:9090` through the SSH tunnel.
- Fetch the raw log file via HTTP: `curl http://127.0.0.1:8080/raw_telemetry.log -o /home/user/raw_telemetry.log`.

Third, write a Bash script `/home/user/process_metrics.sh` that processes `/home/user/raw_telemetry.log`. The raw log format is:
`[TIMESTAMP] IP_ADDRESS HTTP_STATUS RESPONSE_TIME_MS`
Your script must:
- Filter the logs to ONLY include traffic from the three IP addresses mentioned in the voicemail.
- Calculate the average `RESPONSE_TIME_MS` for each hour (ignoring minutes/seconds) for the filtered IPs combined.
- Output a CSV file to `/home/user/dashboard_metrics.csv` with the format: `YYYY-MM-DD HH:00,AVERAGE_RESPONSE_TIME`

Fourth, if the overall percentage of HTTP 5xx errors for these three IPs exceeds the error threshold mentioned in the voicemail, your script must simulate an email alert by writing a properly formatted MIME email to `/home/user/Maildir/new/alert.msg`. It must include a `Subject: Dashboard Alert` and a `To: observability@localhost` header.

Finally, to prevent disk exhaustion, create a logrotate configuration file at `/home/user/logrotate.conf` that rotates `/home/user/raw_telemetry.log` daily, keeps 7 days of backlogs, and compresses old logs. Test it using `logrotate -d`.

Ensure your metrics calculation is as accurate as possible. Your `/home/user/dashboard_metrics.csv` will be evaluated against our internal reference calculation.