You are an automation specialist building a data ingestion workflow. We receive batches of raw telemetry logs from edge devices, but the logs are messy, contain corrupted entries, and are too voluminous for our manual QA team to review entirely.

Your task is to write a Python script at `/home/user/process_logs.py` that processes an existing log file located at `/home/user/raw_logs.txt`.

The script must perform the following pipeline steps:

1. **Extraction (Regex)**: 
   Parse each line to extract the `timestamp`, `device_id`, `status_code`, and `response_time_ms`.
   The valid log format is: `[YYYY-MM-DD HH:MM:SS] <device_id> - STATUS:<status_code> - TIME:<response_time_ms>ms - MSG:<message>`
   Example: `[2023-10-12 08:14:02] DEVICE_A12 - STATUS:200 - TIME:45ms - MSG:Payload delivered`

2. **Validation Gates**:
   Discard any log lines that do not match the format exactly, or fail these quality checks:
   - `status_code` must be exactly three digits (e.g., "200", "404").
   - `response_time_ms` must be a valid non-negative integer (>= 0).
   - `device_id` must start with "DEVICE_" followed by alphanumeric characters.

3. **Summary Statistics**:
   Compute aggregated metrics for the valid logs. Create a CSV file at `/home/user/device_stats.csv` with the headers exactly as: `device_id,log_count,mean_response_time_ms`.
   - Sort the CSV rows alphabetically by `device_id`.
   - `mean_response_time_ms` must be rounded to exactly 2 decimal places.

4. **Stratified Sampling**:
   For downstream ML review, extract a stratified sample of the logs. For *each* valid `device_id`, select exactly the 2 logs with the *lowest* `response_time_ms` (if a device has fewer than 2 valid logs, include all of them).
   - If there is a tie in `response_time_ms`, prefer the log that appeared earlier in the input file.
   - Write these sampled log lines (in their original, unparsed string format) to `/home/user/sampled_logs.txt`.
   - Order the output file primarily by `device_id` (alphabetical), and secondarily by `response_time_ms` (ascending).

Ensure your script runs cleanly without user interaction. You can execute your script to verify its behavior.