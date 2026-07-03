You are acting as an observability engineer to fix our local metrics stack. The stack consists of a backend metrics API, an Nginx reverse proxy serving the dashboard data, a periodic backup job, and a data normalization filter.

Currently, the stack is broken in a few places. Please resolve the following three issues:

**1. Nginx Reverse Proxy Fix (Network & Web Server Setup)**
We have a metrics API running locally on port 8081. An unprivileged Nginx instance is supposed to act as a reverse proxy on port 8080, but it's currently misconfigured and failing to route requests.
- The Nginx configuration file is located at `/home/user/nginx/nginx.conf`.
- Fix the configuration so that any HTTP GET request to `http://localhost:8080/api/metrics` is correctly routed to the backend API at `http://127.0.0.1:8081/`.
- Start the Nginx service in the background using this configuration: `nginx -c /home/user/nginx/nginx.conf`.

**2. Backup Job Fix (Automation & Environment)**
There is a cron job defined for the user that executes `/home/user/scripts/backup.sh` every minute. This script is supposed to copy the metrics database from `/home/user/data/metrics.db` to `/home/user/metrics_backup/metrics.db.bak`.
- Because cron runs with a restricted environment, the backup script is failing or writing to the wrong location (e.g., the home directory root instead of the backup directory).
- Modify `/home/user/scripts/backup.sh` (or the crontab itself) to fix the paths and environment variables so that the database is successfully backed up to `/home/user/metrics_backup/metrics.db.bak`.

**3. The Normalizer Script (Python Implementation)**
Our observability pipeline relies on a Python script to normalize incoming raw log lines into structured JSON. The original script was lost, but we have a compiled reference binary at `/app/oracle_normalizer` that we use for testing.
- You must write a Python 3 script at `/home/user/normalizer.py`.
- The script must read lines from Standard Input (STDIN) one by one and print a single JSON object to Standard Output (STDOUT) for each line.
- The input format is: `[TIMESTAMP] METRIC_NAME: VALUE tags=TAG1,TAG2` (where VALUE is a float).
- The output format must be a JSON object with keys: `ts` (string), `metric` (string), `value` (float), and `tags` (list of strings).
- If a line does not perfectly match this format, the script should output exactly: `{"error": "invalid format"}`
- Your implementation must be bit-exact equivalent to the behavior of `/app/oracle_normalizer`. You can test your script against it by passing various inputs.

Ensure all services are running and your `normalizer.py` script is fully robust against malformed data.