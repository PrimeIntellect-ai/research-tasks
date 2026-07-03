You are a Data Engineer building a compliance-focused ETL pipeline for legacy authentication logs. 

We have a legacy system that generates log files containing sensitive PII. Your task is to write a Python script that streams the data, applies data masking, handles encoding conversions, and computes a rolling window aggregation.

The input file is located at `/home/user/inputs/auth_logs.csv`.
It has three columns: `timestamp` (Unix epoch integer), `ip_address` (IPv4 string), and `email` (string).
Important: The input file is encoded in `cp1252` (Windows-1252).

Write a Python script at `/home/user/etl_pipeline.py` that reads the input file and writes the processed output to `/home/user/outputs/processed_logs.csv` as a UTF-8 encoded CSV.

Your pipeline must perform the following transformations:
1. **Streaming Execution**: Process the file line-by-line or chunk-by-chunk to simulate large-file handling (do not load the entire file into memory at once).
2. **Encoding Handling**: Read the input as `cp1252` and write the output as `utf-8`.
3. **Data Masking (IP)**: Mask the `ip_address` by replacing the last octet with `XXX`. (e.g., `192.168.1.50` becomes `192.168.1.XXX`).
4. **Data Masking (Email)**: Mask the local part of the `email` (everything before the `@`) by keeping only the first character and replacing the rest with `***`. (e.g., `alice.work@example.com` becomes `a***@example.com`).
5. **Rolling Aggregation**: Compute a rolling window metric called `rolling_count`. For each row, calculate how many times the *current masked IP* has appeared in the last 60 seconds (inclusive of the current row). The time window is determined by the `timestamp` column. Only events where `current_timestamp - previous_timestamp <= 60` should be counted. Assume the input file is strictly chronologically sorted.

The output CSV must have a header row and exactly these columns:
`timestamp,masked_ip,masked_email,rolling_count`

Ensure the output directory exists before writing to it. Execute your script to generate the output file.