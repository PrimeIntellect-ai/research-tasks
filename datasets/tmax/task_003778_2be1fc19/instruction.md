You are tasked with organizing and safely rotating project logs for a fast-paced development environment. 

A background process is currently writing sequential log entries to `/home/user/project/data.log`. This process uses file locking (`fcntl.flock` with `LOCK_EX`) to acquire an exclusive lock before writing each line, and releases it immediately after. 

If you try to read, copy, and clear the log file without proper locking, you will cause data loss due to a race condition with the writing process.

Your objective is to write and execute a script (in Bash or Python) at `/home/user/project/rotate.sh` (or `.py`) that performs a safe log rotation. The script must do the following in order:

1. **Safe Extraction**: Acquire an exclusive lock on `/home/user/project/data.log`. While holding the lock, copy its current contents to `/home/user/project/data_snapshot.log` and then truncate (empty) the original `/home/user/project/data.log`. Release the lock immediately after so the background process can continue writing.
2. **Archiving**: Compress `/home/user/project/data_snapshot.log` into a gzip-compressed tar archive named `/home/user/project/archive.tar.gz`.
3. **Integrity Verification & Stream Redirection**: Run a command to verify the integrity of the newly created `archive.tar.gz` (e.g., listing its contents or testing the archive). Redirect the standard output and standard error of this verification command to `/home/user/project/status.txt`.
4. **Symlinking**: Create a symbolic link at `/home/user/project/latest_archive.tar.gz` that points to `archive.tar.gz`.

After writing your script, execute it once. Ensure the background process is not killed and can continue writing to the truncated `data.log`. 

Automated tests will verify that:
- `data_snapshot.log` inside `archive.tar.gz` and the new `data.log` together contain a perfectly continuous sequence of log entries with zero missing lines.
- `latest_archive.tar.gz` is a valid symbolic link pointing to the archive.
- `status.txt` contains the output of the archive integrity check.