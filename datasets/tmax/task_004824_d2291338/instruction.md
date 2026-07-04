You are a log analyst investigating performance anomalies across two microservices.

Your task is to analyze two log files, normalize the data, deduplicate requests, and identify the first point in time where a service exhibits an anomaly (a latency spike).

You have two log files:
1. `/home/user/logs/service_a.jsonl`: JSON Lines format. Each line is a JSON object with keys `timestamp` (ISO8601 string), `req_id` (string), and `latency_s` (float, latency in seconds).
2. `/home/user/logs/service_b.csv`: CSV format. Columns are `timestamp`, `req_id`, and `latency_ms` (integer, latency in milliseconds).

Perform the following data processing pipeline using Python:
1. **Combine & Normalize**: Read both files. Normalize all latencies into milliseconds (`latency_ms`). 
2. **Sort**: Order the combined log entries chronologically by `timestamp` (ascending). 
3. **Deduplicate**: The same `req_id` might be retried or erroneously logged multiple times across both services. Keep only the *first* log entry for each `req_id` (based on chronological order). Discard any subsequent entries with the same `req_id`.
4. **Detect Anomaly**: Process the sorted, deduplicated records chronologically. Maintain a rolling window of the last 3 latencies for *each service separately*. (If a service has fewer than 3 logs so far, use the logs it has). 
An "anomaly" occurs when a service's rolling average latency strictly exceeds `500.0 ms`.
5. **Report**: Find the *very first* log entry (chronologically across the entire sorted timeline) that triggers an anomaly for its service. 

Write the anomaly result to `/home/user/anomaly.json` exactly in this JSON format:
```json
{
  "service": "service_a", 
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "req_id": "..."
}
```
(Note: Use "service_a" or "service_b" for the service name).