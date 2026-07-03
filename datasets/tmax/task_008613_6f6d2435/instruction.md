You are a storage administrator managing disk space and system logs. You have received a full log backup and several differential backup chunks. Recently, a path traversal vulnerability (similar to zip slip) was attempted on your system, and malicious path traversal entries were injected into the logs.

Your task is to consolidate, sanitize, and re-chunk the logs for safe archiving.

Perform the following steps:
1. Merge the differential backup chunks located in `/home/user/logs/diff/` (named `diff_chunk_aa`, `diff_chunk_ab`, `diff_chunk_ac`, etc. in alphabetical order) into a single contiguous differential log.
2. Append this merged differential log to the full backup located at `/home/user/logs/full/system.log` to create a complete log.
3. Sanitize the complete log by writing and executing a Python script at `/home/user/sanitize.py`. The sanitization rules are:
   - Remove entirely any line containing the exact string `MALICIOUS_ENTRY`.
   - In the remaining lines, replace all occurrences of the string `../` with `[REDACTED]`.
4. Split the resulting sanitized log into chunks of exactly 1000 lines each (the last chunk may have fewer lines). Name the output chunks `clean.log.000`, `clean.log.001`, `clean.log.002`, etc., and place them in the `/home/user/logs/clean/` directory. You must create this directory if it does not exist.

Ensure that the final chunks are placed exactly in `/home/user/logs/clean/` with the specified naming convention.