You are a system administrator maintaining a custom application. The application continuously writes logs to `/home/user/app/data.log`. Over time, this file grows too large, and we need a custom rotation and summarization strategy. 

Please perform the following tasks:

1. Create a Python script at `/home/user/rotate_and_summarize.py` that does the following when executed:
   - Checks if the file `/home/user/app/data.log` exists and has a size greater than 0 bytes. If not, the script should exit cleanly without doing anything.
   - Reads the contents of `/home/user/app/data.log`.
   - Extracts all lines that contain the exact uppercase string "ERROR".
   - Appends these extracted lines exactly as they appear to `/home/user/app/error_summary.log`.
   - Rotates the original log file by renaming `/home/user/app/data.log` to `/home/user/app/archive/data_YYYYMMDD_HHMMSS.log` (using the current system time when the script is run for the timestamp).
   - Creates a new, empty `/home/user/app/data.log` file so the application can continue writing to it.

2. Ensure the script is executable.

3. Schedule this script to run daily at exactly midnight (00:00) using the user's `crontab`. The cron entry must execute the Python script using `/usr/bin/python3`.

Constraints:
- You must write the solution in Python using only standard libraries.
- All paths must be absolute as specified.
- Do not modify the application that generates the logs; only manage the files as instructed.