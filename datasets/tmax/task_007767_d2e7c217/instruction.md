I need you to write a Python script to process a messy CSV file containing server metrics. I tried parsing it with standard shell tools, but my pipeline silently dropped rows because the `incident_log` column contains embedded newlines. 

Please write a Python script at `/home/user/process_metrics.py` that reads from `/home/user/raw_metrics.csv` and writes a cleaned, transformed CSV to `/home/user/clean_metrics.csv`.

Here are the processing requirements:
1. **Handle Embedded Newlines**: Correctly parse the CSV, preserving rows where the `incident_log` column has embedded newlines (standard CSV parsing rules apply, these are enclosed in double quotes).
2. **Timestamp Alignment**: The `timestamp` column contains ISO8601 timestamps (e.g., `2023-10-15T08:05:32Z`). Parse these and align/truncate them down to the nearest minute (e.g., `2023-10-15 08:05:00`).
3. **Memory Normalization**: The `memory_usage` column contains strings with mixed units (`GB`, `MB`, `KB`). Convert all these to standard Megabytes (MB) as a float. Use binary prefixes for conversion (1 GB = 1024 MB, 1 MB = 1024 KB). Strip the unit and keep only the number.
4. **Rolling Aggregation**: Sort the data chronologically by the aligned timestamp. Then, calculate a 3-row rolling average for the `cpu_percent` column. For any given row, the rolling average is the mean of the `cpu_percent` for that row and up to 2 immediately preceding rows in the sorted dataset.
5. **Output Format**: The output CSV `/home/user/clean_metrics.csv` must contain the following columns in exactly this order:
   `aligned_minute,cpu_percent,memory_mb,rolling_cpu_3m`
   - `aligned_minute`: String in `YYYY-MM-DD HH:MM:00` format.
   - `cpu_percent`: Float, formatted to exactly 2 decimal places.
   - `memory_mb`: Float, formatted to exactly 2 decimal places.
   - `rolling_cpu_3m`: Float, formatted to exactly 2 decimal places.

Do not include the `incident_log` column in the output. The output CSV must have a header row. You may use standard library modules or `pandas`.

Run your script to generate `/home/user/clean_metrics.csv` before finishing the task.