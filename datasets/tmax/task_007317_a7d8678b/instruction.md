You are an application log analyst. We have a time-series log export located at `/home/user/app_logs.csv` that contains recent server events. A previous attempt to process this file failed silently because the `message` column contains quoted fields with embedded newlines (e.g., multiline stack traces).

Your task is to write a Python script that reads `/home/user/app_logs.csv`, safely parses the CSV (respecting embedded newlines), and applies a specific data processing pipeline.

The input CSV has the following columns: `timestamp,server_id,log_level,message`
(Note: `timestamp` is in ISO 8601 format like `2023-10-01T08:15:30Z`).

Implement the following pipeline and save the output to `/home/user/processed_logs.csv`:

1. **Parse & Deduplicate**: Parse the CSV correctly. Some messages contain newlines. Create an MD5 hash (hexadecimal) of the concatenated string `server_id` + `log_level` + `message` (exactly in that order, with no delimiters added). Deduplicate the dataset based on this hash. Keep *only the first occurrence* of each hash based on the chronological order of the `timestamp`.
2. **Feature Extraction**: Extract the hour of the day from the `timestamp` as an integer (0-23) into a new column called `hour`.
3. **Normalization**: Convert the `log_level` string into an integer severity score in a new column called `severity`:
   - `DEBUG` = 1
   - `INFO` = 2
   - `WARN` = 3
   - `ERROR` = 4
   - `FATAL` = 5
   (Drop any rows that have an unrecognized `log_level`).
4. **Stratified Sampling**: We want to downsample the events for our analytics dashboard. For each unique combination of `(hour, severity)`, keep a maximum of 2 events. Choose the 2 chronologically earliest events in that group.

**Output Specification:**
The final file `/home/user/processed_logs.csv` must:
- Be a valid CSV with headers.
- Contain exactly these columns in this order: `timestamp,server_id,severity,message_hash,hour`
- Be sorted by `timestamp` in ascending chronological order.

Write your script and execute it to generate the final output.