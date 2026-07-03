You are an automation specialist tasked with building a system metrics processing workflow. You have been given a raw dataset of server metrics and need to extract features, compute rolling statistics, and generate a formatted anomaly report.

Your tasks are to:

1. Setup the Environment:
Install any necessary Python libraries (like `pandas` and `jinja2`) to your user environment. 

2. Process the Data:
Create a Python script at `/home/user/analyze_metrics.py`. This script must read `/home/user/data/metrics.csv`. The CSV has the following columns: `timestamp` (ISO 8601 format), `server_id`, `cpu_usage`, and `mem_usage`.
Your script must:
- Sort the data chronologically by `timestamp`.
- Extract a new feature `time_of_day`: "Morning" (06:00-11:59), "Afternoon" (12:00-17:59), or "Night" (18:00-05:59) based on the timestamp (local time, assume UTC).
- Compute rolling statistics: For each `server_id`, calculate a rolling 4-period (current row + 3 previous rows) mean and sample standard deviation (ddof=1) of `cpu_usage`. If a window has fewer than 2 data points, the standard deviation should be 0.0.
- Identify anomalies: An anomaly occurs when a row's `cpu_usage` is strictly greater than `rolling_mean + 1.5 * rolling_std` AND `cpu_usage` is strictly greater than `80.0`.

3. Generate a Report:
Using template-based generation (e.g., Jinja2), output a Markdown report to `/home/user/anomaly_report.md`.
The template must exactly follow this structure:

```markdown
# Server Anomaly Report

## Total Anomalies Detected: {total_anomaly_count}

## Anomaly Details
| Timestamp | Server ID | CPU Usage | Time of Day |
|-----------|-----------|-----------|-------------|
{for each anomaly, sorted chronologically}
| {timestamp} | {server_id} | {cpu_usage rounded to 1 decimal} | {time_of_day} |
```

Run your pipeline so that the final `/home/user/anomaly_report.md` is generated.