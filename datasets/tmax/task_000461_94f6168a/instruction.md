You are an edge computing engineer deploying an IoT monitoring stack on a remote device. You need to write a fully idempotent Python deployment script that sets up a secure web server, an email alert mock server, and a robust scheduled data collection task.

A major source of failure on these IoT devices is that scheduled tasks (cron jobs) run in a stripped-down environment. Previous versions of the data collection script failed to find necessary binaries or wrote output to the wrong relative directories because they relied on `$PATH` and `$HOME` or relative working directories.

Your task is to write a single Python script at `/home/user/deploy_edge.py` that, when executed, will idempotently perform the following steps:

1. **Directory Structure:** Create the following directories if they don't exist:
   - `/home/user/webroot`
   - `/home/user/certs`
   - `/home/user/bin`

2. **Mock Sensor Binary:** Create an executable shell script at `/home/user/bin/mock_sensor` that simply outputs the string: `TEMP=42.5C LOAD=1.2`. (Ensure it has execute permissions).

3. **TLS Certificate:** Generate a self-signed RSA (2048-bit) SSL certificate and private key. Save them exactly at `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`. 

4. **Web Server Wrapper:** Create an executable script at `/home/user/bin/start_web.sh` that launches a Python HTTPS server on `0.0.0.0:8443`. It must serve the contents of `/home/user/webroot` and use the generated TLS certificates. 

5. **Collector Script (The Core Challenge):** Write a Python script at `/home/user/bin/collect.py`. This script will be executed by a cron job (which has a completely empty environment). It must:
   - Execute the `/home/user/bin/mock_sensor` script and capture its standard output.
   - Write the exact captured output into an HTML file at `/home/user/webroot/metrics.html` wrapped in `<h1>` tags (e.g., `<h1>TEMP=42.5C LOAD=1.2</h1>`).
   - Send an email to `admin@edge.local` from `device@edge.local` via SMTP to `127.0.0.1` on port `8025`. The email Subject must be "Alert" and the body must be "Metrics updated".
   - **Constraint:** Because `collect.py` will run via cron, it must not fail when executed via `env -i /usr/bin/python3 /home/user/bin/collect.py`. It cannot rely on relative paths, the `$PATH` variable, or `$HOME`. All paths internally must be absolute, or correctly resolved dynamically without environment variables.

6. **Crontab Setup:** The deployment script must idempotently configure the current user's crontab to run `/usr/bin/python3 /home/user/bin/collect.py` every minute. (e.g. `* * * * * /usr/bin/python3 /home/user/bin/collect.py`). Make sure not to delete other cron entries if they exist, but do not create duplicate entries for `collect.py` if the deploy script is run multiple times.

Write the deployment script to `/home/user/deploy_edge.py` and run it to set up the system. You do not need to start the web server or SMTP server daemons yourself; the verification system will start your `start_web.sh` script and a mock SMTP server on port 8025 to test your collector.