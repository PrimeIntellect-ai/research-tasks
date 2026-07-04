You are acting as a storage administrator who needs to reclaim disk space by purging old logs, but compliance requires us to retain any critical errors from those logs in an anonymized format. 

Your task is to create a C++ pipeline that filters and anonymizes old log files, and a shell script that orchestrates the search, piping, and cleanup.

**Directory Structure & Log Format:**
- Log files are located in `/home/user/logs/`.
- The log files have the extension `.log`.
- Log lines follow this exact format:
  `[YYYY-MM-DD HH:MM:SS] [LEVEL] [IP_ADDRESS] Message body`
  Example: `[2023-10-12 14:32:01] [ERROR] [192.168.1.50] Connection timed out`

**Requirements:**

1. **C++ Filter Program:**
   - Write a C++ program at `/home/user/log_filter.cpp` and compile it to `/home/user/log_filter`.
   - The program must read lines from Standard Input (`stdin`) and write to Standard Output (`stdout`).
   - It should parse the lines and **drop** any line where the `[LEVEL]` is not `[ERROR]` or `[CRITICAL]`.
   - For the retained lines, it must anonymize the IPv4 address by replacing the last octet with `XXX` (e.g., `192.168.1.50` becomes `192.168.1.XXX`).
   - The output must preserve the exact same log format, just with the filtered levels and anonymized IPs.

2. **Orchestration Script:**
   - Write a bash script at `/home/user/process_logs.sh` and make it executable.
   - The script must use `find` to locate all `.log` files in `/home/user/logs/` that were modified **more than 7 days ago**.
   - The script must read the contents of these old log files, pipe them into your compiled `/home/user/log_filter` program, and redirect the final output to `/home/user/critical_archive.log`. (Append or overwrite is fine, assuming it runs once).
   - After successfully archiving the filtered data, the script must delete **only** the old log files it processed.
   - Do not touch log files modified 7 days ago or more recently.

**Execution:**
- You must run your `/home/user/process_logs.sh` script to perform the actual cleanup and archiving.
- We will verify the existence and contents of `/home/user/critical_archive.log` and ensure the correct files in `/home/user/logs/` were deleted.