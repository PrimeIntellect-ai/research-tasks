You are tasked with analyzing a configuration management log that tracks updates across several microservices. 

The system exports these changes to a CSV file located at `/home/user/config_changes.csv`. The file has three columns: `timestamp`, `service_name`, and `config_payload`. 
Because the `config_payload` contains raw JSON and shell script snippets, many fields contain embedded newlines. A naive line-by-line parser will corrupt the data.

Your goal is to process this file, deduplicate redundant updates, calculate a rolling statistic, and save the results to `/home/user/rolling_stats.csv`.

Please implement the following logic:
1. **Parse the CSV correctly**, preserving the embedded newlines within the `config_payload` column. The CSV uses standard double-quote (`"`) quoting.
2. **Deduplicate no-op changes**: For each `service_name`, process the records in chronological order (by `timestamp`). If a row has the exact same `config_payload` as the *most recently retained* row for that same `service_name`, it is considered a no-op duplicate and must be silently dropped. (Note: Only compare against the previously *retained* row for that service).
3. **Calculate Rolling Average**: For each retained row, calculate the length of the `config_payload` in characters. Then, compute the rolling average of this length over a window of the **last 3 retained changes** for that specific `service_name`. 
   - If it is the first retained change for a service, the rolling average is just the length of that payload.
   - If it is the second, it is the average of the first and second.
   - For the third and onwards, it is the average of the most recent three.

**Output Specification:**
Create a standard CSV file at `/home/user/rolling_stats.csv` with the following headers:
`timestamp,service_name,payload_length,rolling_avg_length`

- `timestamp`: The exact timestamp from the input.
- `service_name`: The exact service name from the input.
- `payload_length`: Integer, the character count of the `config_payload`.
- `rolling_avg_length`: Float, the calculated rolling average, rounded to exactly 2 decimal places (e.g., `10.00`, `15.33`).

Make sure the output rows are sorted chronologically by `timestamp`.