You are an automation specialist tasked with debugging a broken log pipeline and detecting a critical system anomaly. 

We have two log files from our web servers:
1. `/home/user/metrics.csv`: Contains minute-by-minute system metrics. Columns: `Timestamp,CPU_Load,Memory_Usage`.
2. `/home/user/events.jsonl`: Contains application events in JSON-lines format. Keys: `Timestamp`, `EventType`, `Message`.

Unfortunately, the upstream logging agent started truncating unicode escape sequences in the `Message` field of `events.jsonl` (e.g., writing `\u002` instead of `\u0020` or using invalid hex characters). Because of this, standard JSON parsers (like Python's `json.loads()`) will throw decoding errors on several lines.

Your task is to:
1. Write a Python script to process these files. You must extract the `Timestamp` and `EventType` from the broken `events.jsonl` file. You can either sanitize the broken unicode sequences or extract the required fields using string manipulation/regex without strict JSON parsing.
2. Read the `metrics.csv` file.
3. Merge the data by `Timestamp`.
4. Detect the anomaly: Find the exact `Timestamp` where the `CPU_Load` is strictly greater than `80.0` AND the count of events with `EventType` equal to `"ERROR"` during that same minute is strictly greater than `5`. There is exactly one such timestamp.
5. Output the result to a new file `/home/user/anomaly_report.json` with the following strict JSON format:
   ```json
   {
     "timestamp": "YYYY-MM-DDTHH:MM",
     "cpu_load": 85.5,
     "error_count": 6
   }
   ```

Requirements:
- Ensure the output file is formatted as valid JSON.
- Use Python for the data processing.