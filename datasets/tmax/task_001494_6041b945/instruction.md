You are a data scientist tasked with cleaning and aggregating a raw event log for a user behavior model. You need to build a multi-stage data processing pipeline. 

The raw data is located at `/home/user/raw_events.jsonl`. It contains JSON objects with the following fields:
`event_id`, `timestamp`, `user_id`, `ip_address`, `duration_sec`, and `event_type`.

Your objective is to generate a final summary CSV file at `/home/user/summary.csv`.

You must create an executable bash script at `/home/user/run_pipeline.sh` that orchestrates this process. You can use standard Linux utilities (like `jq`, `sed`, `awk`) and Python 3. The pipeline must perform the following operations:

1. **Filtering**: Exclude any events where the `event_type` is exactly `"system_ping"`.
2. **Data Masking**: Anonymize the `ip_address` of all remaining events by replacing the last octet (the numbers after the last dot) with `xxx`. For example, `192.168.1.42` becomes `192.168.1.xxx`.
3. **Sorting and Grouping**: Group the filtered and masked events by `user_id`, and ensure they are processed in ascending order of their `timestamp` within each group.
4. **Windowed Aggregation**: For each user, compute a 3-event rolling average of the `duration_sec`. 
   - The rolling window should include the current event and up to two immediately preceding valid events for that user.
   - If a user has fewer than 3 events at a given point, average the available events.
5. **Summary Statistics**: For each user, calculate the final summary.

The final output `/home/user/summary.csv` must contain exactly the following columns in this order:
`user_id,total_valid_events,max_rolling_avg,unique_masked_ips`

Where:
- `max_rolling_avg` is the highest 3-event rolling average computed for that user, rounded to 1 decimal place (e.g., `25.0`).
- `unique_masked_ips` is a semicolon-separated (`;`) list of all unique anonymized IPs used by the user, sorted alphabetically.

Write the scripts, execute your pipeline, and ensure `/home/user/summary.csv` is correctly populated.