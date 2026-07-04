You are a log analyst investigating error patterns across a distributed application. The application generates logs across multiple nodes, and you need to quickly extract unique error signatures per hour to identify when new issues started occurring.

The logs are located in `/home/user/logs/` as multiple `.log` files.
Each log line has the following format:
`[YYYY-MM-DD HH:MM:SS] LEVEL Message`

For example:
`[2023-10-24 14:23:01] ERROR Connection timeout to database`
`[2023-10-24 14:25:12] INFO User login successful`

Your task is to write a Python script at `/home/user/analyze_logs.py` that processes these logs and generates a summary JSON file at `/home/user/hourly_errors.json`.

Requirements for the script:
1. **Parallel Processing**: You must use Python's `multiprocessing` or `concurrent.futures` modules to process the log files in parallel.
2. **Filtering**: Only process lines where the LEVEL is exactly `ERROR`.
3. **Time-based Bucketing**: Group the errors by the hour they occurred. Format the bucket key as `YYYY-MM-DD HH:00:00`.
4. **Hash-based Deduplication**: Within each hourly bucket, deduplicate the error messages using the MD5 hash of the *Message* portion of the log line. 
   - Extract the message (everything after the LEVEL and its following space).
   - Strip any leading or trailing whitespace (including newlines) from the message before hashing.
   - Compute the MD5 hex digest of the UTF-8 encoded message.
5. **Output**: Write the results to `/home/user/hourly_errors.json`. 
   - The JSON should be an object where keys are the hourly buckets (`YYYY-MM-DD HH:00:00`).
   - The values should be a list of the unique MD5 hashes of the errors that occurred in that hour.
   - Sort the list of hashes alphabetically.
   - Sort the keys (hours) alphabetically.
   - Format with `indent=2`.

Run your script to generate the final `/home/user/hourly_errors.json` file.