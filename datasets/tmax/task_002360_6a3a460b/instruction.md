You are acting as a backup administrator responsible for archiving and sanitizing server logs. 

We have a legacy backup archive located at `/home/user/backups/raw_logs.tar.gz`. This archive contains several multi-line log files. Due to a bug in the old logging system, some records are missing mandatory error codes, and we accidentally ingested logs from a decommissioned server.

Your task is to sanitize these logs and create a new, clean archive.

Here are the exact requirements:

1. **Extract and Verify**: Extract the archive into `/home/user/processing/`. 
2. **Transform Logs**: Every `.log` file in the archive consists of multi-line records. Each record starts with `[START_RECORD]` and ends with `[END_RECORD]`.
   - **Rule A (Removal)**: If a record contains the line `Server: DEPRECATED_SRV`, you must delete that *entire* multi-line record (from `[START_RECORD]` to `[END_RECORD]` inclusive).
   - **Rule B (Insertion)**: For all remaining records, if the record does NOT contain a line starting with `ErrorCode: `, you must insert the line `ErrorCode: 0000` exactly on the line immediately preceding `[END_RECORD]`.
3. **Atomic Operations**: You must process these files using temporary files and atomic `mv` operations (e.g., process to a `.tmp` file, then `mv` it over the original file) to simulate safe in-place editing.
4. **Re-archive**: Compress the sanitized log files back into a new archive located exactly at `/home/user/backups/clean_logs.tar.gz`. Ensure the archive structure matches the original (i.e., extracting it should yield the `.log` files in the same relative paths).
5. **Reporting**: Create a text file at `/home/user/backups/summary.txt` containing the exact total number of `[START_RECORD]` occurrences across all final `.log` files in the `/home/user/processing/` directory, printed as a single integer.

Do all your scripting and transformations using standard Bash utilities (awk, sed, grep, etc.).