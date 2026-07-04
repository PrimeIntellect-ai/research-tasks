You are acting as a backup administrator. A log rotation script on our servers often races with the writing process, leaving some log files with truncated, invalid lines at the end. 

We need to archive all fatal error logs from our application servers.

Your task is to:
1. Recursively traverse the directory `/home/user/server_logs/` to find all log files. The files will either end in `.log` (plain text) or `.log.gz` (gzip compressed).
2. Read through all these files and attempt to parse each line as a JSON object.
3. Because of the race condition, some lines are incomplete/invalid JSON. You must safely ignore any line that cannot be parsed as valid JSON.
4. For all *valid* JSON records, filter and keep only the ones where the `"level"` key is exactly `"FATAL"`.
5. Sort these filtered records ascending by their integer `"id"` key.
6. Write the sorted JSON lines to a single file at `/home/user/fatal_errors.jsonl` (one JSON object per line, no extra whitespace).
7. Finally, package this file into a compressed tar archive at `/home/user/fatal_backup.tar.gz` containing exactly the file `fatal_errors.jsonl` at its root.

You can write a Python script to accomplish this or use shell commands.