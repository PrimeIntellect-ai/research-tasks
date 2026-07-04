You are an AI assistant helping a data analyst process a mix of event logs.

The analyst has received raw event data in two different formats, located in `/home/user/data/`:
1. `events_1.csv` - A CSV file with columns: `timestamp,user_id,action`
2. `events_2.jsonl` - A JSON-lines file where each line is a JSON object with keys: `timestamp,user_id,action`, and sometimes an optional `note` field.

**The Problem:**
Some lines in the `events_2.jsonl` file contain malformed unicode escape sequences in the `note` field (e.g., `\uZZZZ`), which cause standard JSON parsers to throw a `json.decoder.JSONDecodeError`.

**Your Task:**
Write a Python script at `/home/user/process_events.py` and run it to perform the following ETL process:

1. **Multi-format Reading:** Read both `events_1.csv` and `events_2.jsonl`. 
2. **Error Handling & Logging:** If a line in the JSONL file fails to parse due to a JSON decoding error, catch the exception, write a warning to `/home/user/output/error.log` in the exact format `ERROR:events_2.jsonl:<line_number>` (where line_number starts at 1), and skip that line. Do not stop the pipeline.
3. **Time-based Bucketing & Aggregation:** Parse the `timestamp` field (which is in ISO 8601 format like `2023-10-15T08:15:30Z`) and truncate it to the start of the hour (e.g., `2023-10-15 08:00:00`). Aggregate the data to count the number of occurrences of each `action` per hour bucket.
4. **Writing:** Output the aggregated results to a CSV file at `/home/user/output/hourly_summary.csv` with exactly these columns in order: `hour_bucket,action,count`. Sort the output CSV first by `hour_bucket` (ascending), then by `action` (ascending). 

**Constraints:**
- Do not use third-party libraries like `pandas`; stick to Python's standard library (`csv`, `json`, `datetime`, `collections`, etc.).
- Ensure the `hour_bucket` is formatted as `YYYY-MM-DD HH:00:00`.
- Create the `/home/user/output/` directory if it does not exist.