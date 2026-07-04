You are a storage administrator responsible for managing disk space on a critical Linux server. The primary log directory, `/home/user/logs/`, is growing out of control. You need to write a Python script to enforce a strict log retention and archiving policy.

Please write and execute a Python script located at `/home/user/log_manager.py` that performs the following operations:

1. Target Directory: Scan `/home/user/logs/` for any files ending in `.log`.
2. Size Threshold: Identify files that contain strictly more than 10,000 lines. Files with 10,000 lines or fewer must be completely ignored and left unmodified.
3. Splitting and Archiving: For each file exceeding the threshold:
   - Keep exactly the last 1,000 lines of the file in the original location (`/home/user/logs/<filename>`).
   - Prepend the string `### LOG ROTATED ###\n` as the absolute first line of this active log file (making it 1,001 lines total).
   - The remaining earlier lines (everything before the last 1,000 lines) must be extracted for archiving.
4. Large-Scale Text Editing: While extracting the older lines for archiving, filter out and permanently delete any line that contains the exact substring `[IGNORE]`.
5. Compression: Compress the filtered archived lines using `gzip` and save the output to `/home/user/archive/<filename>.gz`. (You must create the `/home/user/archive/` directory if it does not exist).
6. Summary Report: Create a text file at `/home/user/summary.txt` that lists each processed file and the exact number of lines that were written to its compressed archive (after the `[IGNORE]` filtering). The format for each line in `summary.txt` should be exactly: `<filename>: <archived_line_count>` (e.g., `app.log: 8500`). Ensure the files are listed in alphabetical order.

Once you have written the script, execute it so the log files are properly rotated and the system state reflects your successful run.