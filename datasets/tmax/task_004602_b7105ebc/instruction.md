You are acting as a backup administrator archiving system data. We need to securely archive a server log file, but it contains sensitive IP addresses that must be redacted before storage. Additionally, to allow for fast temporal lookups in the future, we need a binary index mapping timestamps to file offsets.

Your task is to write and execute a Python script located at `/home/user/archive_log.py` that processes the input log file `/home/user/server.log`.

The input log file `/home/user/server.log` has lines in the following format:
`YYYY-MM-DD HH:MM:SS [IP_ADDRESS] Log message text...`
Example:
`2023-10-15 08:23:45 [192.168.1.50] User login successful`

Your Python script must perform the following actions:
1. **Redaction**: Read the input log file line by line (using streaming I/O to handle potentially large files) and redact any IP address inside the brackets, replacing it with the exact string `REDACTED`. The brackets themselves must remain. 
   Example transformed line: `2023-10-15 08:23:45 [REDACTED] User login successful\n`
2. **Atomic Write**: Write the redacted lines to a temporary file, and once completely written, atomically rename it to `/home/user/sanitized.log`.
3. **Binary Indexing**: While processing the redacted file, construct a binary index. For each line, parse the timestamp (`YYYY-MM-DD HH:MM:SS`) into a Unix epoch timestamp (UTC). Write a 16-byte binary record for each line consisting of:
   - An 8-byte unsigned integer (little-endian) representing the Unix epoch timestamp.
   - An 8-byte unsigned integer (little-endian) representing the byte offset of the *start* of that line in the *sanitized* log file.
4. Write this binary data to a temporary file and atomically rename it to `/home/user/index.bin`.

Ensure that `/home/user/archive_log.py` is executable and run it to produce `/home/user/sanitized.log` and `/home/user/index.bin`. Use standard library Python modules only. Assume the system timezone is UTC for timestamp parsing.