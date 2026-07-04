You are tasked with building a small Python data processing pipeline to analyze configuration change logs. 

A configuration management system writes events to a JSON-Lines file located at `/home/user/config_events.jsonl`. Each line represents a configuration event and is intended to be a valid JSON object with the following schema:
`{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "service": "service_name", "action": "update", "details": "..."}`

However, a known bug in the logging system sometimes injects malformed unicode escape sequences (e.g., `\u12X4`) into the `details` field, causing standard JSON parsers to throw a `JSONDecodeError`.

Write a Python script at `/home/user/process_configs.py` that implements a multi-stage pipeline:
1. **Validation Gate (Extraction):** Read `/home/user/config_events.jsonl` line by line. Attempt to parse each line as JSON.
2. **Quarantine:** If a line fails to parse due to a JSON decoding error, catch the error and append the raw, unmodified line to `/home/user/quarantine.jsonl`.
3. **Time-based Bucketing (Transformation):** For all successfully parsed lines, bucket the events by the hour in which they occurred. Do this by truncating the minutes and seconds of the `timestamp` to `00:00Z` (e.g., `2023-10-25T14:32:01Z` becomes `2023-10-25T14:00:00Z`).
4. **Aggregation:** Count the number of valid configuration events per service, per hour.
5. **Load:** Output the final aggregated data to `/home/user/hourly_summary.json`.

The output file `/home/user/hourly_summary.json` must be a pretty-printed JSON file (indentation 2) with the following structure:
```json
{
  "YYYY-MM-DDTHH:00:00Z": {
    "service_name_1": <integer_count>,
    "service_name_2": <integer_count>
  }
}
```

Run your script so that `/home/user/hourly_summary.json` and `/home/user/quarantine.jsonl` are generated successfully.