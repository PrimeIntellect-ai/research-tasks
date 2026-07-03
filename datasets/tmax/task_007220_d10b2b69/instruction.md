You are a data analyst troubleshooting performance issues for a web service. You have been given two disparate data sources that need to be cleaned, aligned, and merged into a single timeline.

Here are your input files:
1. `/home/user/cpu_metrics.csv`: A CSV containing CPU usage reported every minute. However, the telemetry agent is buggy, so some minutes have missing values (blank `cpu_usage`). Timestamps are in ISO 8601 format (e.g., `2023-10-01T10:00:00Z`).
2. `/home/user/app_logs.txt`: An unstructured text log file from the application layer. Lines contain timestamps in `[MMM DD HH:MM:SS]` format and occasionally mention request latency. Example: `[Oct 01 10:00:15] INFO - Request processed in 120ms`

Your objective is to write a Python script (or multi-stage bash/Python pipeline) that processes these files and produces a final merged dataset at `/home/user/merged_analysis.csv`.

Here are the requirements for the data processing pipeline:

**1. Structured Information Extraction:**
Parse `/home/user/app_logs.txt`. Extract the timestamp and the latency value (in milliseconds) from any line that contains the word "latency" or the phrase "processed in Xms".
Note: The log timestamps do not specify a year or timezone. You must assume the year is `2023` and the timezone is `UTC`.

**2. Timestamp Alignment & Aggregation:**
Since the log events occur at random seconds, you must aggregate the extracted latencies into 1-minute buckets (by truncating the seconds) to align with the `cpu_metrics.csv` timeline. Calculate the *mean* average latency for each minute.

**3. Interpolation and Imputation:**
Load `/home/user/cpu_metrics.csv`. For any missing `cpu_usage` values, use **linear interpolation** based on the surrounding time points to fill in the gaps. 

**4. Merging & Output Format:**
Merge the interpolated CPU metrics and the aggregated log latencies on the minute-level timestamps. 
Write the result to `/home/user/merged_analysis.csv`.
The final CSV must have exactly these headers: `timestamp,cpu_usage,avg_latency`.
- `timestamp`: formatted exactly as `YYYY-MM-DD HH:MM:00`
- `cpu_usage`: rounded to 1 decimal place (e.g., `45.5`)
- `avg_latency`: rounded to 1 decimal place (e.g., `150.0`). If there were no log events for a given minute, leave the `avg_latency` field completely empty (e.g., `2023-10-01 10:03:00,50.0,`).

You may install `pandas` or any standard libraries to complete this task.