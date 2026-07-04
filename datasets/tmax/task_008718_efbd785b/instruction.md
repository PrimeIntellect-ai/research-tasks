You are a backup administrator tasked with cleaning up a sensitive data leak in an archived log backup. 

There is an existing archive located at `/home/user/backups/app_logs.tar.gz` which contains several log files. Unfortunately, an application bug caused sensitive credentials to be written to these logs. The leaking lines always begin with the exact string `CREDENTIAL_LEAK:`. 

Since the archive could theoretically be very large, you must process it streamingly without extracting the entire archive to disk.

Your task is to:
1. Write a Python script at `/home/user/sanitize_archive.py` that reads `/home/user/backups/app_logs.tar.gz`.
2. Streamingly read the contents, remove any lines that start with `CREDENTIAL_LEAK:`, and stream the sanitized files into a new temporary tar.gz file.
3. Verify the integrity of the new archive (ensure it is a valid gzip-compressed tar archive).
4. Atomically move the temporary archive to `/home/user/backups/sanitized_app_logs.tar.gz`.
5. Count the total number of sensitive lines you removed across all files, and write this count to `/home/user/backups/report.txt` in the exact format: `Removed: <COUNT> lines` (e.g., `Removed: 45 lines`).

Constraints:
- Do not extract the files to the filesystem. Everything must be processed in memory / streamingly.
- Ensure the modified files in the new tarball have the same filenames as in the original tarball.
- The new archive must be valid and readable. 
- You must use Python to perform the archive sanitization. You may execute your script from the terminal.