You are a backup administrator responsible for safely archiving application errors from a live environment. The application continuously writes to log files in `/home/user/app_logs/` and aggressively rotates them. These logs contain multi-line error traces.

Your task is to write a bash script at `/home/user/archive_errors.sh` that performs a safe, compressed extraction of recent errors. 

The script must meet the following requirements exactly:
1. Find all `.log` files in the directory `/home/user/app_logs/` that have been modified within the last 2 days (use `find`'s mtime or similar metadata-based search).
2. To ensure predictable output, process the found files in alphabetical order based on their full file paths.
3. The active application locks these files exclusively when writing. To avoid reading partially written lines and risking corruption, your script MUST acquire a shared lock (using `flock -s`) on each log file before reading it.
4. From these locked files, extract all multi-line error blocks. An error block begins with a line containing exactly `[ERROR]` and ends with a line containing exactly `[END ERROR]`. Both the start and end lines must be included in the output.
5. Stream the extracted error blocks from all processed files directly into a gzip compressed file located at `/home/user/archive/recent_errors.gz`. (Create the `/home/user/archive/` directory if it does not exist).
6. The script should be executable (`chmod +x`).

The log files are already present in the `/home/user/app_logs/` directory. You should create the script, ensure it is executable, and then run it once so that `/home/user/archive/recent_errors.gz` is generated. 

Do not use any external scripting languages like Python or Perl; you must use bash and standard shell utilities (e.g., `find`, `sort`, `flock`, `sed`, `awk`, `grep`, `gzip`).