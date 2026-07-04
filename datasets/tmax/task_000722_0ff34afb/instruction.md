You are tasked with debugging a regression in a data processing script using `git bisect` and your Bash skills.

You have been provided with a Git repository at `/home/user/log_processor` which contains a Bash script named `process_logs.sh`. The script is designed to parse log files and output a count of each log level (e.g., INFO, ERROR, WARN).

A regression was introduced recently (within the last 200 commits). The script now incorrectly counts log levels if the log message itself contains words that look like log levels (e.g., if an INFO log message contains the word "ERROR", it incorrectly counts an extra ERROR).

Here is a sample log file located at `/home/user/test_log.txt`:
```text
[2023-10-01 12:00:00] [INFO] Server started
[2023-10-01 12:01:00] [INFO] User encountered an ERROR
[2023-10-01 12:02:00] [WARN] Disk space low
[2023-10-01 12:03:00] [ERROR] Process crashed
```

For the above file, the correct output should be exactly:
```text
ERROR: 1
INFO: 2
WARN: 1
```

The buggy version produces:
```text
ERROR: 2
INFO: 2
WARN: 1
```

Your tasks are:
1. Navigate to `/home/user/log_processor`.
2. The commit tagged `v1.0` is known to be good. The current `HEAD` (master) is known to be bad.
3. Use `git bisect` (and optionally a test script for automation) to find the exact commit that introduced the bug.
4. Write the full 40-character SHA-1 hash of the first bad commit to a file named `/home/user/bad_commit.txt`.
5. Fix the bug in the `process_logs.sh` script currently at `HEAD`. Ensure it properly extracts the log level only from the second set of brackets `[LEVEL]` and handles any arbitrary log messages.
6. Save your fixed script to `/home/user/fixed_process_logs.sh`. Ensure it has execute permissions.

Constraints:
- Only use standard Bash built-ins, coreutils, and standard Unix tools (grep, awk, sed, etc.).
- Do not modify the Git history of the repository.