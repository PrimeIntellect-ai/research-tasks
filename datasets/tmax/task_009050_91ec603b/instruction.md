You are a data scientist cleaning up time series logs from a failed ETL job. The job was retried multiple times, resulting in duplicate records in our raw log file.

You have been provided a JSON-Lines file at `/home/user/raw_data.jsonl`.
Each line is a JSON object representing a time series data point with the following fields:
- `timestamp` (ISO-8601 string)
- `metric_id` (string, e.g., "CPU_Load", "mem_usage")
- `value` (numeric)
- `message` (string, may contain Unicode characters like Japanese or French text)

Your task is to process this file using only standard Bash shell tools (like `jq`, `awk`, `sort`, etc.) to produce a clean CSV file and a summary report.

Here are the requirements:
1. **Normalize**: Convert all `metric_id` values to strictly lowercase.
2. **Deduplicate**: Because of ETL retries, there are duplicate records for the exact same `timestamp` and normalized `metric_id`. You must keep ONLY the **last** occurrence of each `(timestamp, metric_id)` pair as it appears in the original file.
3. **Format & Sort**: Write the cleaned data to `/home/user/clean_data.csv`. 
   - The file must be a standard comma-separated CSV (without a header row). 
   - The columns must be: `timestamp,metric_id,value,message` (ensure string fields with commas or special characters are properly quoted, standard `jq -r '@csv'` behavior is perfect).
   - The output must be sorted ascending by `timestamp`, and then ascending by `metric_id`.
4. **Summary Report**: Generate a text file at `/home/user/report.txt` using exactly the following template:
```
ETL Cleanup Report
------------------
Total Clean Records: [COUNT]
Unique Metrics: [COMMA_SEPARATED_LIST]
```
Replace `[COUNT]` with the total number of records in `clean_data.csv`.
Replace `[COMMA_SEPARATED_LIST]` with an alphabetically sorted, comma-separated list of the unique, normalized `metric_id`s found in the clean data (e.g., `cpu_load,disk_io,mem_usage`). There should be no spaces after the commas.

Complete the task using terminal commands. Do not write a Python or Node.js script.