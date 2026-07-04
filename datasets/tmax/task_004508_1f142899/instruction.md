You are a log analyst investigating anomalous patterns in system metrics. We are deploying a new real-time log ingestion and anomaly detection pipeline, but the infrastructure is partially misconfigured, and the anomaly detection logic is missing.

Your task has two parts:

### Part 1: Fix the Ingestion Pipeline (Multi-Service Compose)
We have a local setup consisting of two services:
1. **Nginx**: Running as a reverse proxy, configured via `/app/nginx.conf`.
2. **Flask Log API**: A backend service running on `127.0.0.1:5000` that handles file validation and storage.

Currently, Nginx is not correctly routing ingestion traffic to the Flask backend. 
- Edit `/app/nginx.conf` so that any `POST` requests to `http://127.0.0.1:8080/ingest` are correctly proxied to `http://127.0.0.1:5000/ingest`.
- You must restart Nginx or reload its configuration for the changes to take effect. Nginx is managed via the command `nginx -c /app/nginx.conf`.

### Part 2: Build the Time-Series Anomaly Detector
The Flask backend expects an external script to perform deep inspection on the incoming time-series log batches. 
Write a Python script at `/home/user/detector.py`. 

The script will be invoked by the Flask app as follows:
`python3 /home/user/detector.py <path_to_json_file>`

The JSON file contains an array of chronological metric logs. Example:
```json
[
  {"timestamp": 1690000000, "latency": 42.5, "cpu_load": 0.35},
  {"timestamp": 1690000005, "latency": 48.0, "cpu_load": 0.38},
  ...
]
```

Your `detector.py` must perform the following time-series analysis:
1. **Windowed Aggregation**: Calculate the rolling mean of the `latency` field over a window of exactly 3 consecutive logs (e.g., logs 1-2-3, logs 2-3-4).
2. **Feature Extraction**: 
   - Extract **Feature A**: The maximum value of these rolling means. (If there are fewer than 3 logs, Feature A is 0.0).
   - Extract **Feature B**: The overall average of the `cpu_load` field across all logs in the file.
3. **Distance Computation**: Compute the Euclidean distance between the extracted feature vector `(Feature A, Feature B)` and a known healthy baseline vector `(50.0, 0.4)`.
4. **Classification**: 
   - If the Euclidean distance is **strictly greater than 15.0**, the batch is anomalous ("evil"). Your script must exit with status code `1`.
   - Otherwise, the batch is normal ("clean"). Your script must exit with status code `0`.

Ensure your Python script relies only on standard libraries or `numpy`/`pandas` if installed, and handles parsing the JSON correctly. The testing suite will send several batches through your Nginx endpoint to verify the full pipeline end-to-end.