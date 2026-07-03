You are an incident response log analyst. We have a messy server log file at `/home/user/raw_server_logs.txt` containing interleaved application events. 

Your task is to write a Python script at `/home/user/process_logs.py` to extract, normalize, deduplicate, and load specific error events into a SQLite database.

Requirements for the Python script:
1. **Filter and Extract**: Read `/home/user/raw_server_logs.txt`. Process only lines that contain `ERROR:`. The log format is `[YYYY-MM-DD HH:MM:SS.mmm] <LEVEL>: <message> - ID:<user_id>`.
2. **Timestamp Alignment**: Parse the timestamp of the error and align it to the *start of the minute*. For example, `[2023-10-25 14:32:45.123]` must become `2023-10-25 14:32:00`.
3. **Hash-based Deduplication**: Some errors spam the log multiple times within the same minute. Create an MD5 hash of the exact string formatted as `"{aligned_timestamp}|{message}|{user_id}"` (e.g., `"2023-10-25 14:32:00|Connection timeout|usr_123"`). Deduplicate the records by this MD5 hash, keeping only the first occurrence of each unique hash.
4. **Database Export**: Create a SQLite database at `/home/user/errors.db`. Create a table named `error_logs` with the following schema:
   - `hash_id` (TEXT, Primary Key)
   - `timestamp` (TEXT) - The minute-aligned timestamp
   - `message` (TEXT)
   - `user_id` (TEXT)
   Insert the deduplicated records into this table.

Once your script is written, run it to generate the `/home/user/errors.db` file. Ensure the database is closed properly so the data is flushed to disk.