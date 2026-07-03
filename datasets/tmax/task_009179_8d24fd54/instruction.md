You are a data analyst working with time series data from legacy IoT sensors. The sensors export CSV files with different character encodings, containing some malformed data and overlapping timestamps.

Your task is to create a robust data processing pipeline using Bash. 

There is a directory at `/home/user/data/` containing two files:
1. `sensor_a.csv` (Encoded in UTF-16LE)
2. `sensor_b.csv` (Encoded in ISO-8859-1)

The CSV format for both files is: `sensor_id,timestamp,value`

Write a bash script at `/home/user/process_metrics.sh` that does the following when executed:
1. Reads both CSV files and normalizes their character encoding to UTF-8.
2. Filters out any rows where the `timestamp` (the second column) does not perfectly match the ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-01T12:00:00Z`). Use standard grep/regex for this.
3. Sorts the combined valid records by timestamp in chronological (ascending) order.
4. Deduplicates the records based *only* on the timestamp column. If multiple records have the same timestamp, keep only the first one that appears in the sorted output.
5. Writes the cleaned, UTF-8 encoded, deduplicated output to `/home/user/clean_metrics.csv`.
6. Generates a summary report by writing exactly this template to `/home/user/summary.txt`:
   `Processing complete. A total of [N] valid, unique time series points were extracted.`
   (Replace `[N]` with the actual number of lines written to `clean_metrics.csv`).

Ensure your script `/home/user/process_metrics.sh` is executable.

Finally, you need to schedule this pipeline. Create a file named `/home/user/cron_schedule` containing exactly one line: the crontab entry required to execute `/home/user/process_metrics.sh` every Tuesday at 4:15 AM. (Assume the cron daemon runs as `user`).

Constraints:
- Only use standard Bash built-ins, coreutils, and standard Unix CLI tools (e.g., `iconv`, `grep`, `sort`, `awk`, `sed`).
- Do not use Python, Perl, or other scripting languages.