You are a log analyst investigating performance degradation on a web server. The server logs are stored on a simulated remote mount at `/opt/remote/web.log`. You need to build a data pipeline to fetch this data, extract features, detect anomalies, and schedule the process.

Please complete the following steps:

1. Create a bash script at `/home/user/run_pipeline.sh` that performs the following:
   - Copies `/opt/remote/web.log` to a local working directory `/home/user/data/` (create this directory if it doesn't exist).
   - Executes a Python script located at `/home/user/log_analyzer.py` (which you will write next).

2. Write the Python script `/home/user/log_analyzer.py`. This script must:
   - Read the local log file `/home/user/data/web.log`.
   - Parse each line to extract the Timestamp, IP address, and ResponseTime (in milliseconds). The logs have a custom format:
     `[{TIMESTAMP}] IP: {IP} | User-Agent: {UA} | ResponseTime: {TIME}ms`
   - Implement an anomaly detection algorithm: An anomaly is defined as any request where the `ResponseTime` is strictly greater than 3 times the average `ResponseTime` of the **immediately preceding 5 requests**. (If there are fewer than 5 preceding requests, it cannot be considered an anomaly).
   - Write all detected anomalies to a CSV file at `/home/user/anomalies.csv`. The CSV must have the following exact header and format:
     `Timestamp,IP,ResponseTime`
     (ResponseTime should be just the integer value, e.g., 150, not 150ms).

3. Schedule the pipeline:
   - Add a cron job for the current user to run `/home/user/run_pipeline.sh` exactly every 5 minutes. (Make sure the script has execute permissions).

4. Finally, execute `/home/user/run_pipeline.sh` manually once so that `/home/user/data/web.log` is copied and `/home/user/anomalies.csv` is generated for verification.

Ensure your Python script relies only on standard library modules (e.g., `csv`, `re`).