You are acting as a storage administrator to reclaim disk space from inactive log files. 

Write a Python script at `/home/user/reclaimer.py` and run it to perform the following operations:

1. Recursively traverse the directory `/home/user/data/logs`.
2. Find all files ending in `.log`.
3. For each `.log` file, check if there is a corresponding lock file. A lock file has the exact same name but with `.lock` appended (e.g., if the file is `server.log`, the lock file would be `server.log.lock`).
4. If a `.lock` file exists for a given `.log` file, it means an active process is writing to it. **Do not** modify this `.log` file.
5. If there is **no** `.lock` file, the log file is inactive. You must:
   a. Append its contents to a central incremental backup archive at `/home/user/archived_logs.bak`.
   b. Before writing to the archive file, acquire an exclusive file lock on `/home/user/archived_logs.bak` using Python's `fcntl.flock` to ensure concurrent runs of this script wouldn't corrupt the backup. Release the lock after writing.
   c. The format appended to the archive must be exactly:
      ```
      --- <absolute_path_to_log_file> ---
      <contents_of_the_log_file>
      ```
      (Ensure there is a newline after the file contents if it doesn't end with one, but don't add extra newlines if it does).
   d. After appending the contents to the archive, **truncate** the original `.log` file to 0 bytes to reclaim disk space. Do not delete the file.

Execute your script so that `/home/user/archived_logs.bak` is generated and the inactive log files are truncated.