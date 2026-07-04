You are a storage administrator managing disk space on a Linux server. There is a directory containing highly compressed historical logs at `/home/user/storage/logs/`. 

To understand how much space is consumed by fatal crash dumps, you need to analyze the structured log data inside these archives. The logs are stored in a nested archive format to save space: each outer archive is a `.tar.gz` file, which contains one or more `.zip` files, which in turn contain JSON files containing the actual log entries.

Write a Python script at `/home/user/analyze_logs.py` that does the following:
1. Searches `/home/user/storage/logs/` for all `.tar.gz` files.
2. Reads the nested `.zip` files and the inner `.json` files **in memory** (without extracting them to the disk, to avoid filling up the disk space).
3. Parses the JSON data. Each JSON file contains a list of dictionary objects. 
4. Identifies all log entries where the key `"level"` equals `"FATAL"`.
5. Sums the integer value of the `"size_bytes"` key for those FATAL entries, per outer `.tar.gz` archive.
6. Outputs the final aggregated results to a CSV file at `/home/user/fatal_sizes.csv`.

The output CSV must have exactly two columns: `archive_name` (just the base name of the `.tar.gz` file, e.g., `logs_2023.tar.gz`) and `total_fatal_bytes` (the integer sum of sizes for FATAL errors in that archive). The CSV must include a header row, and the rows must be sorted alphabetically by `archive_name`. If an archive has no FATAL errors, its total should be `0`.

Execute your script to ensure the `/home/user/fatal_sizes.csv` file is generated correctly.