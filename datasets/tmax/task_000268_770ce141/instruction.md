You are acting as a storage administrator to manage disk space on a legacy storage volume.

The directory `/home/user/storage_pool` contains hundreds of verbose log files (`.vlog`) scattered across a deep, nested directory structure. These files are consuming too much space and need to be transformed into a compressed, structured format, while safely ignoring files that are currently being written to by active processes.

Your task is to write and execute a Python script that performs the following steps:

1. **Recursive Traversal:** Find all `.vlog` files inside `/home/user/storage_pool` and its subdirectories.
2. **Concurrency/Lock Check:** Some `.vlog` files are currently in use by active systems. A file is considered "in use" and MUST BE SKIPPED entirely if there is a corresponding lock file with the exact same name but `.lock` appended (e.g., `app_data.vlog` is locked if `app_data.vlog.lock` exists in the same directory). 
3. **Format Conversion & Transformation:** For every `.vlog` file that is NOT locked:
   - Read the file. Each line in the `.vlog` file follows this exact verbose format:
     `[<LEVEL>] <YYYY-MM-DD HH:MM:SS> - User: <username> - Action: <action_name> - Status: <status_message>`
     *(Example: `[INFO] 2023-10-01 12:45:00 - User: admin - Action: system_backup - Status: completed successfully`)*
   - Parse each line into a JSON object with keys: `level`, `timestamp`, `user`, `action`, and `status`.
   - Write these JSON objects (one per line, JSONL format) into a new GZIP-compressed file. The new file must be created in the exact same directory as the original, with the `.vlog` extension replaced by `.jsonl.gz`.
4. **Space Reclamation:** Delete the original `.vlog` file ONLY after successfully creating the `.jsonl.gz` file.
5. **Audit Logging (with File Locking):** As your script processes files, it must append a record to a central audit log located at `/home/user/audit_log.jsonl`. Because your script should ideally process files concurrently (or be safe to run as multiple instances), you MUST use `fcntl` exclusive file locking (`fcntl.flock(f, fcntl.LOCK_EX)`) when appending to `/home/user/audit_log.jsonl`.
   Each line appended to the audit log must be a JSON object containing:
   - `original_file`: The absolute path of the original `.vlog` file.
   - `compressed_file`: The absolute path of the new `.jsonl.gz` file.
   - `lines_processed`: Integer count of log lines successfully converted.

Ensure your Python script is executed and completes the transformation before finishing the task.