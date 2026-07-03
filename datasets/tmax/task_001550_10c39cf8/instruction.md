You are an observability engineer tasked with fixing and optimizing a poorly written log collection pipeline. 

In `/home/user/observability/`, there is a multi-service stack simulating a monitoring environment:
1. `log_generator.py` (Service A): Generates mock Nginx access logs to `/home/user/observability/logs/access.log`.
2. `dashboard_server.py` (Service B): An HTTP API running on port 8080 that reads `/home/user/observability/metrics/summary.json` to power a dashboard.
3. `scheduler.sh` (Service C): A supervisor script that runs `/home/user/observability/collector.sh` every 5 seconds. To simulate a strict `cron` environment, `scheduler.sh` completely strips environment variables and changes the working directory to `/tmp/` before invoking the script.

Currently, the dashboard is completely blank. The `collector.sh` script has two major problems:
1. **Pathing Issue:** It uses relative paths and relies on environment variables, causing it to write `summary.json` to the wrong location when invoked by `scheduler.sh`. 
2. **Performance Issue:** It is currently written using a naive Bash `while read` loop. In production, `access.log` can grow to millions of lines. The current script is incredibly slow and cannot keep up with the log volume.

Your tasks:
1. **Fix the Pathing:** Modify `/home/user/observability/collector.sh` so that it always reads from `/home/user/observability/logs/access.log` and writes the output directly to `/home/user/observability/metrics/summary.json`, regardless of the caller's working directory or environment.
2. **Optimize the Pipeline:** Rewrite the parsing logic in `collector.sh` using efficient text processing tools (e.g., `awk`). 
3. **Format Requirements:** The script must produce a strictly formatted JSON file. It needs to calculate the total counts for each HTTP status code block (2xx, 3xx, 4xx, 5xx) and the sum of the response bytes. The log format is standard combined: `IP - - [Date] "METHOD /path HTTP/1.1" STATUS BYTES`.
    The output in `/home/user/observability/metrics/summary.json` must look exactly like this (whitespace doesn't matter, but keys do):
    ```json
    {
      "status_2xx": 1500,
      "status_3xx": 0,
      "status_4xx": 42,
      "status_5xx": 3,
      "total_bytes": 10485760
    }
    ```
4. **Error Handling:** If the log file does not exist or is empty, the script should output all zeros for the counts and bytes.

You must modify `/home/user/observability/collector.sh`. You do not need to restart the services, `scheduler.sh` will automatically pick up your changes on its next loop. Your solution must be highly optimized—an automated verifier will test your script against a massive log file, and it must complete processing in under 1.5 seconds.