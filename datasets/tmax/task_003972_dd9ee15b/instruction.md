You are an AI assistant helping a data analyst process some messy log files.

There is a CSV file located at `/home/user/system_logs.csv` containing server event logs. Standard shell tools are failing to process it properly because the `message` column frequently contains embedded newlines and commas.

Write a Python script at `/home/user/process_logs.py` and execute it to process this file and generate a summary CSV.

The requirements for the script are as follows:
1. Correctly read the CSV file (columns: `event_id`, `timestamp`, `message`), correctly handling embedded newlines and commas in the `message` field.
2. Filter the rows to keep only those where the `message` starts with the exact regex pattern `^CRITICAL: .*` (after stripping leading/trailing whitespace).
3. Align the `timestamp` (which is in ISO 8601 format, e.g., `2023-10-15T14:35:12Z`) to the start of the hour (e.g., `2023-10-15T14:00:00Z`).
4. Calculate the string similarity of the `message` to the reference string: `"CRITICAL: Disk failure detected in /dev/sda1"`. Use Python's built-in `difflib.SequenceMatcher(None, message, reference).ratio()`.
5. Keep only the events where this similarity ratio is `>= 0.60`.
6. Group these filtered events by the aligned hour timestamp and count the number of events per hour.
7. Sort the aggregated results chronologically by the aligned timestamp (ascending).
8. Write the results to `/home/user/critical_hourly_summary.csv` with exactly two columns: `hour_timestamp` and `event_count`.

You must use standard Python libraries only (`csv`, `re`, `datetime`, `difflib`, etc.). Ensure your script is executed so the output file is generated.