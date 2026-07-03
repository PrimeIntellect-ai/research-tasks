You are acting as a storage administrator to reclaim disk space from redundant backup copies. 

The backup system recently completed an incremental backup, but due to a configuration error, it copied all files completely instead of creating hard links for the files that hadn't changed.

Here is the current system state:
- A JSON registry file at `/home/user/backups.json` contains metadata about the backups, including the paths to the `base` backup directory and the `inc` (incremental) backup directory.
- A multi-line log file at `/home/user/sync.log` contains records of the files processed during the backup. Every record spans exactly three lines:
  ```
  FILE: <filename>
  SIZE: <bytes>
  STATUS: <SUCCESS|FAILED>
  ```

Your task is to write and execute a Python script (alongside any shell commands you wish) to perform the following operations:
1. Parse `/home/user/backups.json` to extract the paths for the base and incremental backup directories.
2. Parse `/home/user/sync.log` to identify all files that have `STATUS: SUCCESS`.
3. For every successfully processed file, check if it exists in both the base and incremental directories. If the contents are exactly identical, deduplicate it by deleting the copy in the incremental directory and creating a hard link to the file in the base directory.
4. Generate a CSV report at `/home/user/dedup_report.csv` with exactly two columns: `filename,saved_bytes`. Include only the files that were successfully hardlinked. The `saved_bytes` should be the size of the deduplicated file.
5. Create a symbolic link at `/home/user/latest_backup` pointing to the incremental backup directory.

Do not modify the contents of the files in the base backup. Ensure your CSV exactly matches the header format `filename,saved_bytes`.