You are a system administrator tasked with creating a custom lightweight logging mechanism for a specific server environment. Since this server lacks standard logging daemons, you must build a custom solution using C and Bash.

Please complete the following steps:

1. **Create a C program for timestamp generation**:
   Write a C program at `/home/user/write_timestamp.c` and compile it to `/home/user/write_timestamp`. 
   The program must:
   - Read the current system time.
   - Print the time to standard output in exactly this format: `YYYY-MM-DD HH:MM:SS %Z` (where `%Z` is the timezone abbreviation, e.g., `JST` or `UTC`).
   - Output a trailing newline.
   
2. **Create a Bash wrapper script with log rotation**:
   Write a bash script at `/home/user/logger_script.sh`. Ensure it has execute permissions.
   When executed, the script must:
   - Set the timezone environment variable `TZ` to `Asia/Tokyo`.
   - Set the locale environment variable `LC_ALL` to `C`.
   - Check the length of the log file `/home/user/server.log`. If the file exists and has 3 or more lines, rename it to `/home/user/server.log.old` (overwriting any existing `.old` file) to simulate log rotation.
   - Execute the compiled `/home/user/write_timestamp` program and append its output to `/home/user/server.log`.

3. **Configure the schedule**:
   Create a text file at `/home/user/cron_schedule` that contains exactly one line. This line should be a standard crontab entry that schedules `/home/user/logger_script.sh` to run every 15 minutes (e.g., at minute 0, 15, 30, and 45 of every hour). Use absolute paths for the script.

Ensure all files are created in `/home/user/` and have the appropriate permissions.