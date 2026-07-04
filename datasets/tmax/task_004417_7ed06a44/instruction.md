You are assisting a network security engineer who is analyzing a recent incident involving an insecure file upload service. 

There are two parts to this task:

**Part 1: Code Remediation**
You have been provided with the source code for the file upload handler located at `/home/user/upload_handler.c`. This program takes a filename as a command-line argument and writes some default data to it inside the `/home/user/uploads/` directory. However, it is vulnerable to a Path Traversal attack (CWE-22).
1. Audit the C code and identify the vulnerability.
2. Modify `/home/user/upload_handler.c` to enforce a strict filename policy: if the provided filename contains any forward slashes (`/`) or the parent directory sequence (`../`), the program must print exactly `ERR: Invalid filename\n` to standard output and exit with status code `1` before doing any file operations.
3. Compile the fixed code to an executable named `/home/user/upload_handler` (using `gcc /home/user/upload_handler.c -o /home/user/upload_handler`).

**Part 2: Intrusion Detection and Redaction**
A network traffic log containing upload requests is located at `/home/user/traffic.log`.
1. Scan this log file for malicious upload attempts that tried to exploit the path traversal vulnerability (i.e., the requested filename in the log contains `../` or `/`).
2. For these malicious records, redact the sensitive API key. Replace the actual key value after `KEY:` with the exact string `[REDACTED]`.
3. Save ONLY the redacted malicious log lines to `/home/user/redacted_alerts.log`. Keep the original formatting of the line intact, modifying only the API key.

Make sure `/home/user/upload_handler` is compiled and `/home/user/redacted_alerts.log` is created with the correct contents when you are finished.