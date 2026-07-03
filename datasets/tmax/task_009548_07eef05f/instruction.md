You are an automation specialist tasked with creating a robust bash-based data processing pipeline. We have a system that dumps unstructured application logs into a specific directory, and we need to reliably extract, deduplicate, and log unique error messages.

Please perform the following steps:

1. Create a bash script at `/home/user/process_errors.sh`. Make sure it is executable.
2. The script must read all `.log` files in the directory `/home/user/incoming/`.
3. Extract structured error information from the log lines. Specifically, extract only the substring starting with `ERROR_CODE:` followed by one or more digits, a space, `MESSAGE:`, and the rest of the line. (e.g., from `[INFO] 2023-10-24 ERROR_CODE:500 MESSAGE:Internal Server Error`, extract exactly `ERROR_CODE:500 MESSAGE:Internal Server Error`).
4. To ensure we do not process duplicate errors (even across different log files or repeated runs), implement hash-based deduplication:
   - For each extracted error string, compute its SHA-256 hash (use the string exactly as extracted, without trailing newlines during computation, e.g., `echo -n "$extracted_string" | sha256sum | awk '{print $1}'`).
   - Check if this hash exists in `/home/user/processed_hashes.log`.
   - If the hash is NOT in the log, append the extracted error string as a new line to `/home/user/unique_errors.txt` AND append the new hash as a new line to `/home/user/processed_hashes.log`.
5. Finally, schedule this script to run automatically. Install a cron job for the current user that executes `/home/user/process_errors.sh` exactly at minute 0 of every hour.

Requirements:
- Only use standard bash built-ins and core utilities (`grep`, `awk`, `sed`, `sha256sum`, etc.).
- The files `/home/user/unique_errors.txt` and `/home/user/processed_hashes.log` should be created by your script if they don't exist.
- Ensure the crontab exactly matches the schedule `0 * * * *` with the absolute path to the script.