You are a log analyst investigating latency patterns in our web services. We have a multi-service setup where a simulated log emitter continuously appends logs to `/app/logs/events.log`. 

Your task is to create a Python HTTP API that processes this log file on-demand and returns aggregated time-series insights.

Here is what you need to do:
1. Write and run a Python web service (e.g., using Flask, FastAPI, or the standard `http.server`) that listens on `127.0.0.1:8080`.
2. Implement a `GET /stats` endpoint that reads the `/app/logs/events.log` file.
3. The log lines have the format: `YYYY-MM-DDTHH:MM:SSZ | LEVEL | latency=XXXms | message`
   Example: `2023-10-25T10:00:00Z | ERROR | latency=150ms | DB timeout`
4. The endpoint must process the logs with the following rules:
   - **Extraction & Validation:** Parse the latency value. Ignore any lines where latency is missing, negative, or not an integer (e.g., `latency=-5ms` or `latency=NaNms` should be skipped).
   - **Rolling Statistics:** Calculate the simple average of the *last 3 valid latency values* found in the file.
   - **Stratified Sampling:** For each log level (INFO, WARN, ERROR, etc.) present in the valid logs, extract the exact raw text of the *latest* valid log line for that level.
5. The `GET /stats` endpoint must return a JSON response exactly matching this schema:
   ```json
   {
     "rolling_avg_3": 125.0,
     "latest_by_level": {
       "INFO": "2023-10-25T10:05:00Z | INFO | latency=100ms | Request successful",
       "ERROR": "2023-10-25T10:00:00Z | ERROR | latency=150ms | DB timeout"
     }
   }
   ```

A lightweight Nginx proxy is already configured to route traffic from `127.0.0.1:8000/api/stats` to your service at `127.0.0.1:8080/stats`. The verification suite will test the API by sending an HTTP request to `http://127.0.0.1:8000/api/stats` and validating the JSON response.

Leave your Python server running in the background so the verifier can test it.