As a backup administrator, I need you to help me audit our archived system logs to identify failed backup jobs that were missed by our old alerting system. 

We have simulated a series of mounted backup archives in the directory `/home/user/archive_mounts/`. Inside this directory, there are multiple server folders, each containing deeply nested directories with `.log` files.

Your task is to write a Python script that recursively traverses `/home/user/archive_mounts/` and parses all `.log` files. 

The logs are written in a multi-line format where every new log record strictly begins with a timestamp in brackets, like this:
`[YYYY-MM-DD HH:MM:SS] LEVEL - Message`

Any lines following this header (without a timestamp prefix) belong to that log record (e.g., stack traces or command outputs). 

You need to find all log records where the severity level is `FATAL` and the message starts with `Backup job failed`. 

Once you find these records, extract the timestamp of the error and the absolute path of the file it was found in. Save your findings to a CSV file located at `/home/user/failed_backups.csv`. 

The CSV must have the following exact headers:
`timestamp,absolute_file_path`

Sort the CSV rows chronologically by timestamp (oldest first). If multiple errors have the exact same timestamp, sort them alphabetically by file path.

Ensure your script handles the multi-line nature of the logs correctly, though for this specific report we only need the timestamp from the header line of the matched record.