You are tasked with fixing a fragile data pipeline for our time-series telemetry system. 

We have a legacy C-based aggregator located at `/app/ts_aggregator`. This tool reads JSON-Lines (JSONL) telemetry logs from `stdin` and outputs a reshaped, wide-format CSV. However, this binary is completely undocumented, stripped of symbols, and heavily prone to crashing. Specifically, it suffers from a fatal flaw: it will instantly segmentation fault if it encounters improperly formatted unicode escape sequences in the JSON payload (e.g., orphaned surrogate halves like `\uD800` or invalid hex like `\u12XZ`) or if the JSON keys are missing.

Your task is to write a Python sanitizer script at `/home/user/cleaner.py` that acts as a robust filter before data reaches the aggregator. 

The script must:
1. Accept a single file path as a command-line argument: `python3 /home/user/cleaner.py <path_to_jsonl>`
2. Read the file line-by-line.
3. Parse each line as JSON. The expected schema for each line is:
   - `ts`: An ISO-8601 timestamp string.
   - `sensor_id`: A string representing the sensor.
   - `msg`: A text payload.
4. Validate the JSON. If a line cannot be parsed as JSON, lacks any of the required keys, or contains invalid/broken unicode escape sequences in the `msg` field, you MUST completely drop the line.
5. For lines that pass validation, normalize the `msg` field by converting it to lowercase and removing any punctuation (keep only alphanumeric characters and spaces).
6. Sort all valid, normalized records chronologically by the `ts` field.
7. Print the resulting JSON-Lines to `stdout`, one valid JSON object per line.

Do not output anything else to `stdout` (no debug prints), as this stream will be piped directly into `/app/ts_aggregator` in our production environment. You can assume the input files will fit in memory for the sorting phase. Ensure your Python script is executable and has the correct imports.