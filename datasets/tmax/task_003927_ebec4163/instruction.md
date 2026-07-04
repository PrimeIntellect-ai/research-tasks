You are acting as a backup operator tasked with migrating and testing restores from a legacy archival system. We recently recovered the proprietary backup chunk decoder, but it is provided only as a stripped ELF binary (`/app/legacy_decode`). We need a modern, fast, and maintainable replacement written in C++.

Your objectives are as follows:

1. **Reverse-Engineer the Decoder:**
   Analyze the behavior of `/app/legacy_decode`. It reads data from standard input, decodes it, and writes to standard output. 
   Write a C++ program at `/home/user/new_decode.cpp` and compile it to `/home/user/new_decode`. Your program must behave *exactly* the same as the legacy decoder for any valid input byte stream. 

2. **Environment & Automation Setup:**
   Create a bash wrapper script at `/home/user/restore_wrapper.sh` that does the following:
   - Sources a profile file `/home/user/.backup_profile` (which you must create and populate with `export BACKUP_MODE=RESTORE` and `export ARCHIVE_ROOT=/tmp/restores`).
   - Reads all `.chk` files in a directory provided as the first argument.
   - Passes the contents of each file through `/home/user/new_decode`.
   - Appends a log line to `/home/user/restore.log` formatted exactly as: `[YYYY-MM-DD HH:MM:SS] Decoded chunk: <filename> - <number_of_bytes_output> bytes`.

3. **Log Configuration and Rotation:**
   Since this restore process will run continuously on thousands of chunks, the log file will grow rapidly.
   Create a local logrotate configuration file at `/home/user/logrotate.conf` that targets `/home/user/restore.log`. It must:
   - Rotate the log daily.
   - Retain exactly 7 backlogs.
   - Compress old logs.
   - Ensure the log is rotated if it exceeds 10MB in size, regardless of the daily schedule.

Ensure your C++ code is highly efficient and perfectly matches the output of the stripped binary.