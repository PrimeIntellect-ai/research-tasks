You are acting as a support engineer troubleshooting a crashed data-processing service for a client. The client reported that their Python-based service failed abruptly, and now their metrics database appears corrupted. 

Your goals are to collect diagnostics to identify the root cause of the crash, recover the customer's data, and prepare a diagnostic report.

Perform the following steps:
1. The service script is located at `/home/user/service.py`. When you run it, it immediately fails. Use system call tracing (e.g., `strace`) to figure out what file it is attempting to load right before it crashes. The script attempts to load a dynamically linked library/plugin that is missing, which causes the failure. Identify the exact absolute path of this missing file.
2. The customer's database is located at `/home/user/metrics.db`. Due to the crash, the database disk image is malformed/corrupted. Use standard SQLite recovery techniques (e.g., the `.recover` or `.dump` command in the `sqlite3` CLI) to salvage the data and restore it into a new, working database file at `/home/user/metrics_recovered.db`.
3. Write a short Python script at `/home/user/check_db.py` that connects to `/home/user/metrics_recovered.db` and queries the number of rows in the `events` table.
4. Finally, create a summary report for the client at `/home/user/diagnostic_report.txt` with exactly two lines:
   - Line 1: The absolute path of the missing file that caused `service.py` to crash (found in step 1).
   - Line 2: The exact integer number of rows successfully recovered from the `events` table.

Do not include any other text in `/home/user/diagnostic_report.txt`.