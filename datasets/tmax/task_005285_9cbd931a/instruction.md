You are a log analyst investigating access patterns to an internal application. You need to build an automated ingestion pipeline and an API server to expose log statistics.

Your task consists of the following steps:

1. **Fix and Install the Vendored Package:**
   There is a custom log parsing library located at `/app/vendored/py-log-parser-1.0.0`. It contains a deliberate typo that prevents it from running. Find the typo in `pylogparser/core.py`, fix it, and install the package locally so it can be imported as `pylogparser` in Python.

2. **Log Processing Script:**
   Write a Python script at `/home/user/process_logs.py`. It should read all `.log` files in the directory `/home/user/raw_logs/` (which contains standard access logs).
   For each line in each file:
   - Use the fixed `pylogparser.parse_line(line)` function to extract a dictionary containing `ip`, `timestamp`, `method`, and `endpoint`.
   - **Normalize** the `endpoint` by stripping any query parameters (e.g., `/api/data?user=123` must become `/api/data`).
   - Bulk insert these normalized records into a SQLite database at `/home/user/logs.db` in a table named `access_logs` (columns: `ip`, `timestamp`, `method`, `endpoint`).

3. **Pipeline Scheduling:**
   Create a bash script at `/home/user/run_pipeline.sh` that executes your `process_logs.py` script.
   Then, write a crontab configuration file to `/home/user/cron_config.txt` that schedules `/home/user/run_pipeline.sh` to run exactly at the top of every hour (e.g., minute 0). Install this using the `crontab` command.

4. **API Server:**
   Write and start a Python HTTP server at `/home/user/server.py`. It must run in the background and listen continuously on `127.0.0.1:8888`.
   - Protocol: HTTP
   - Endpoint: `GET /api/ip-stats`
   - Response format: `application/json`
   - Content: A JSON dictionary where the keys are IP addresses and the values are the total number of requests made by that IP, as queried from your `/home/user/logs.db`.

To complete the task, ensure the database is fully populated from the raw logs and that your server is running and bound to `127.0.0.1:8888` before finishing.