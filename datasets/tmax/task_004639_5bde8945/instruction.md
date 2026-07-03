You are tasked with building a data processing pipeline to analyze how server configuration changes impact resource utilization. You have been provided with two messy data sources: an unstructured text log of configuration changes and a CSV of irregular CPU utilization metrics.

Your goal is to extract the configuration changes, remove duplicates, normalize and smooth the CPU metrics, and join the two datasets to produce a final report.

**Data Sources:**
1. **Config Logs (`/home/user/data/config_updates.log`)**: An unstructured text file containing log entries. Some lines contain configuration updates.
2. **Metrics CSV (`/home/user/data/metrics.csv`)**: A CSV file with columns `timestamp`, `server_id`, and `cpu`. The timestamps are recorded at irregular intervals, and there are gaps in the data.

**Requirements:**

1. **Regex Extraction & Parsing:**
   Write a Python script to parse `/home/user/data/config_updates.log`. Extract lines that represent configuration updates. These lines follow this exact pattern (ignoring surrounding text/noise):
   `[{YYYY-MM-DD HH:MM:SS}] [UPDATE] {server_id} : {config_key} -> {config_value}`
   Extract the timestamp, `server_id`, `config_key`, and `config_value`. 

2. **Hash-Based Deduplication:**
   Configuration managers sometimes retry applying configs, resulting in duplicate logs. Create a SHA-256 hash of the concatenated string `{server_id}{config_key}{config_value}`. If you encounter multiple log entries with the exact same hash, keep only the *first* occurrence (based on chronological order in the file) and discard the rest.

3. **Resampling & Gap-Filling:**
   Process `/home/user/data/metrics.csv`. For each `server_id` independently:
   - Truncate (floor) the `timestamp` to the start of the minute (e.g., `10:05:42` becomes `10:05:00`).
   - Group by the 1-minute intervals and calculate the `mean` of the `cpu` values for that minute.
   - Forward-fill any missing 1-minute intervals. If a minute has no data, use the value from the most recent previous minute for that server. 

4. **Rolling Statistics:**
   After resampling and gap-filling, compute a 3-minute rolling average of the CPU metric for each server. The rolling window should include the current minute and the previous 2 minutes. If 3 minutes of history are not available (e.g., at the start of the series), calculate the average over the available minutes.

5. **Joins & Output:**
   For each deduplicated configuration change:
   - Floor its timestamp to the minute.
   - Find the smoothed (3-minute rolling average) CPU value for that `server_id` at that specific minute.
   - If no CPU data exists for that server at or before that minute (meaning it cannot be forward-filled), drop the record.

Output the final joined dataset as a JSON array of dictionaries to `/home/user/config_impact.json`. Each dictionary must have the following keys:
- `"timestamp"`: The original, exact timestamp of the config change (string, format `"YYYY-MM-DD HH:MM:SS"`).
- `"server_id"`: (string)
- `"config_key"`: (string)
- `"config_value"`: (string)
- `"smoothed_cpu"`: The 3-minute rolling average CPU value at the floored minute of the config change, rounded to 2 decimal places (float).

Sort the output JSON array chronologically by the exact config change timestamp.