You are a backup administrator tasked with creating an efficient, incremental log extraction tool. An active application writes logs to `/home/user/service.log`. Some log entries are single lines, while others (especially errors) span multiple lines.

Write a Python script at `/home/user/extract_errors.py` that does the following:
1. **State Management & File Locking:** It must maintain a state file at `/home/user/backup.state` containing a single integer representing the byte offset up to which the log has been processed. To prevent concurrent backup jobs from corrupting the state, use `fcntl.flock(fd, fcntl.LOCK_EX)` on the state file while reading and updating it. If the state file doesn't exist, assume an offset of 0.
2. **Memory-Mapped I/O:** Open `/home/user/service.log` and use the `mmap` module to read the file starting from the offset found in the state file. 
3. **Multi-line Parsing:** Parse the new data. Every log record starts with a timestamp and severity in the format: `[YYYY-MM-DD HH:MM:SS] LEVEL ` (e.g., `[2023-10-25 14:00:01] INFO ` or `[2023-10-25 14:00:05] ERROR `). Any subsequent lines that do not start with `[` belong to the preceding log record (e.g., stack traces).
4. **Incremental Backup:** Extract all complete `ERROR` records (including their multi-line stack traces) and append them exactly as they appear to `/home/user/error_archive.log`.
5. **Update State:** Write the new byte offset (the end of the processed data) back to `/home/user/backup.state` before releasing the lock. 

To complete the task:
1. Create the `/home/user/extract_errors.py` script.
2. Run it once to process the existing `/home/user/service.log`.

Note: The system will test your script by appending new data to `service.log` and running your script a second time concurrently to verify locking and incremental differential behavior. Make sure your script handles trailing newlines properly and only records complete log events.