You are a data engineer tasked with building a lightweight ETL pipeline to process raw server metrics. 

You have been provided with a directory `/home/user/data/` containing a messy log file named `raw_metrics.jsonl`. You also have a template file at `/home/user/templates/host_summary.tpl`.

Your task is to write and execute a Python script that processes these metrics, aggregates them, and generates text reports.

Here are the requirements for your ETL pipeline:

**Phase 1: Extraction & Cleaning**
1. Read `/home/user/data/raw_metrics.jsonl`. Each line is a JSON object.
2. Discard any JSON objects that are missing the `host` key or the `timestamp` key.
3. Discard any objects where `cpu_usage` or `memory_mb` is null, missing, or cannot be parsed as a float.
4. Normalize the `timestamp` field into an integer representing Unix epoch seconds. 
   - Some timestamps are already Unix epochs (integers or strings like `"1685581200"`).
   - Some are ISO8601 strings (e.g., `"2023-06-01T01:00:00Z"`). Assume all string dates are in UTC.
5. Deduplicate the records. If multiple records have the exact same `host`, `timestamp` (after normalization), `cpu_usage`, and `memory_mb`, keep only one.

**Phase 2: Bucketing & Aggregation**
1. Group the cleaned records by `host`.
2. For each host, bucket the records into 1-hour windows based on the normalized timestamp. A 1-hour window starts at the hour boundary (e.g., epoch `1685581200` which is 01:00:00). To find the window, floor the epoch timestamp to the nearest multiple of 3600.
3. For each host and each 1-hour window, calculate:
   - The average `cpu_usage` (rounded to exactly 2 decimal places).
   - The maximum `memory_mb`.

**Phase 3: Template-Based Generation**
1. Read the template file located at `/home/user/templates/host_summary.tpl`.
2. For each distinct `host`, generate a report by replacing the placeholders in the template.
   - Replace `{host}` with the host name.
   - Replace `{num_windows}` with the total number of 1-hour windows that have data for this host.
   - Replace `{metrics_list}` with a newline-separated list of metrics for each window, sorted chronologically by the window's starting epoch timestamp.
     Each line in `{metrics_list}` must strictly follow this format:
     `Window: <window_epoch> | Avg CPU: <avg_cpu> | Max Mem: <max_mem>`
3. Ensure the `/home/user/output/` directory exists.
4. Save each generated report to `/home/user/output/<host>_report.txt`.

Ensure your Python script creates the output files successfully. You may install standard libraries if necessary, though standard Python 3 is sufficient.