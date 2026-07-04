You are a storage administrator managing a server where a rogue log rotation script recently raced with the primary logging process. As a result, several gzip-compressed log archives were abruptly truncated while they were being written. 

Your goal is to recover the critical system errors from these partially corrupted log files.

The log files are located in `/home/user/app_logs/`. All files end with `.gz`.
Inside these archives, each line is a JSON object.

Your task is to:
1. Extract and read all readable JSON lines from every `.gz` file in `/home/user/app_logs/`, safely ignoring and recovering from any decompression errors or truncated data streams.
2. Filter the recovered logs to find only those where the `"status"` key is exactly `"FATAL"`.
3. Create a CSV file at `/home/user/fatal_alerts.csv` containing the parsed data.
4. The CSV must have exactly two columns: `timestamp` and `error_id`. Keep the header row: `timestamp,error_id`.
5. Order the rows chronologically by the `timestamp` column (oldest to newest).

Ensure your solution writes the final file exactly to `/home/user/fatal_alerts.csv`.