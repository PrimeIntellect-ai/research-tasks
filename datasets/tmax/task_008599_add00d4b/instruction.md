You are tasked with building a robust data processing pipeline to analyze configuration change logs from a fleet of servers. 

The input data is located at `/home/user/data/config_changes.jsonl`. It contains JSON-lines formatted logs, but the system that generated them had a bug: some log lines contain malformed unicode escape sequences (e.g., `\u002"`, `\uXX"`) which causes standard JSON parsers to crash. Additionally, some telemetry data (`cpu_load`) was dropped in transit and appears as `null`.

You must write a script (or a combination of shell commands and code in Python/Node/etc.) to perform the following steps:

1. **Character Encoding/Format Handling:** 
   Read the JSONL file. Before parsing each line as JSON, detect and fix any malformed unicode escape sequences (specifically, `\u` followed by fewer than 4 valid hex digits before a double quote or another character). Replace the entire malformed `\u...` sequence with a single question mark `?`. Then parse the line as JSON. Keep track of how many lines required this fix.

2. **Interpolation and Imputation:**
   For each unique `server`, sort the records chronologically by `timestamp`. Some records have a `null` value for `cpu_load`. You must impute these missing values using linear interpolation based on the timestamps (treat timestamps as Unix epoch seconds for interpolation). If the first or last record for a server is missing, backfill or forward-fill using the nearest available value. Keep track of how many `cpu_load` values were imputed.

3. **Feature Extraction:**
   Create a new integer field called `high_load`. Set it to `1` if the (possibly imputed) `cpu_load` is strictly greater than `80.0`, and `0` otherwise.

4. **Data Sampling and Stratification:**
   For each unique `server`, extract exactly the top 2 records with the highest `cpu_load`. If there is a tie in `cpu_load`, prioritize the record with the oldest (earliest) `timestamp`. 

5. **Output and Pipeline Logging:**
   - Save the sampled data as a CSV file at `/home/user/output/sampled_changes.csv` with the exact following header: `server,timestamp,config_val,cpu_load,high_load`. The rows should be sorted alphabetically by `server`, then descending by `cpu_load`. Format `cpu_load` to exactly 2 decimal places.
   - Create a log file at `/home/user/output/pipeline.log` containing exactly these three lines:
     `Total lines read: <count>`
     `Malformed lines fixed: <count>`
     `Missing values imputed: <count>`

Ensure your solution handles edge cases and runs entirely within the `/home/user` environment.