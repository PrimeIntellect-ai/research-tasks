You are acting as a Site Reliability Engineer (SRE). We have a monitoring setup where our alerting script needs to send downtime alerts via an internal SMTP server that is only accessible through a specific SSH bastion. 

Your task consists of three main parts:

1. **Fix and Install a Vendored Package**
We use a custom, internal Python package called `tunneled_smtp_client` to route emails through SSH tunnels. The source code for version 0.9 is pre-vendored at `/app/vendor/tunneled_smtp_client-0.9/`.
However, there is a known bug in `tunneled_smtp_client/connection.py`. A developer accidentally hardcoded the SSH port to `22` in the `connect()` method, which overrides the configured port. 
Find the bug, fix it so it respects the `ssh_port` attribute of the class, and install the package locally in the user environment (`pip install --user -e /app/vendor/tunneled_smtp_client-0.9/`).

2. **Reverse Engineer an Alert Formatter**
Our monitoring system requires alert emails to be formatted in a very specific way. We have a compiled reference binary at `/app/oracle_format_alert` that correctly formats these alerts.
You must write a Python script at `/home/user/format_alert.py` that takes a single command-line argument containing a JSON-encoded list of service statuses, and prints the EXACT same output as the oracle.

The JSON schema for the input is a list of objects, each with:
- `service` (string): The name of the service.
- `status` (string): Either "up" or "down".
- `latency_ms` (integer): The latency in milliseconds (or -1 if down).
- `error` (string or null): An error message if down, or null if up.

Example input:
`'[{"service": "api-gateway", "status": "down", "latency_ms": -1, "error": "timeout"}, {"service": "auth-service", "status": "up", "latency_ms": 12, "error": null}]'`

You can test your script against the oracle by passing the same JSON string to both:
`/app/oracle_format_alert <json_string>`
`python3 /home/user/format_alert.py <json_string>`
Your Python script's standard output must be bit-for-bit identical to the oracle's output for any valid input.

3. **Scheduled Task Setup**
Create a cron job configuration file at `/home/user/monitoring_cron` that schedules a bash script `/home/user/run_monitor.sh` to run every 5 minutes. Load this file into the current user's crontab. Ensure the cron configuration has the correct syntax.