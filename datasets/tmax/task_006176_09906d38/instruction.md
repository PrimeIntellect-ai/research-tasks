I need you to help organize and consolidate some application logs from a project I'm working on. The application generates Write-Ahead Logs (WAL) and periodically rotates and compresses them. Because of a bug in our rotation script, the logs are scattered across a deep directory structure under `/home/user/app_logs`. Some are plain text (`.wal`), and some are gzip-compressed (`.wal.gz`).

I need you to write a Python script that will:
1. Recursively traverse `/home/user/app_logs` and find all files ending in `.wal` and `.wal.gz`.
2. Parse the contents of these logs. The format of every line is a pipe-delimited string: `SEQ_ID|TIMESTAMP|LEVEL|MESSAGE`.
   - `SEQ_ID` is an integer.
   - `TIMESTAMP` is an ISO8601 string.
   - `LEVEL` is a log level (e.g., INFO, DEBUG, WARN, ERROR, FATAL).
   - `MESSAGE` is a free-form text message.
3. Extract only the log entries where the `LEVEL` is exactly `ERROR` or `FATAL`.
4. Sort the extracted log entries globally in ascending order based on their `SEQ_ID`.
5. Write the sorted entries back out to a single gzip-compressed stream at `/home/user/critical_logs.gz`. The format must remain exactly the same as the input (`SEQ_ID|TIMESTAMP|LEVEL|MESSAGE\n`).

Please create and run a Python script to accomplish this. Once you have generated `/home/user/critical_logs.gz`, your task is complete.