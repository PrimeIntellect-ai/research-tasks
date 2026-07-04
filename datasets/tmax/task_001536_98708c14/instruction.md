You are acting as a log analyst investigating access patterns while ensuring data privacy. 

You need to create a Python script `/home/user/process_logs.py` to process a time-series access log file located at `/home/user/input_logs.csv`, and then schedule it to run automatically.

The input CSV has the following headers: `timestamp,ip_address,method,endpoint,user_agent`.

Your Python script must perform the following ETL steps:
1. **Normalization**: Convert all HTTP methods in the `method` column to uppercase (e.g., 'get' -> 'GET').
2. **Anonymization (Data Masking)**: Mask the `ip_address` by replacing the last two octets with `X.X`. For example, `192.168.1.5` must become `192.168.X.X`.
3. **Hash-based Deduplication**: Create a SHA-256 hash of a string combining the masked IP, normalized method, endpoint, and user agent (format: `IP|METHOD|ENDPOINT|USERAGENT`). Use this hash to deduplicate the rows. If multiple rows produce the same hash, keep ONLY the row with the earliest `timestamp`.
4. **Output**: Save the cleaned and deduplicated data to `/home/user/cleaned_logs.csv` (keeping the original column names and order, but with the modified IP and method). Sort the final output by `timestamp` in ascending order.
5. **Pipeline Logging**: The script must append exactly one line to `/home/user/pipeline.log` every time it runs, using the exact format:
   `[YYYY-MM-DD HH:MM:SS] Processed <N> original rows into <M> deduplicated rows.` 
   (Replace YYYY-MM-DD HH:MM:SS with the current UTC time, `<N>` with the input row count excluding the header, and `<M>` with the output row count).

Finally, schedule this script using the user's `crontab` to run at the top of every hour (minute 0). Ensure the crontab executes the script using `/usr/bin/env python3`.