You are acting as a network security engineer investigating a recent compromise. You have a web server access log from an API gateway that handles file uploads. You suspect an attacker successfully exploited a path traversal vulnerability in the upload handler to drop a malicious authentication token and bypass the authentication flow.

You have been provided with the log file at `/home/user/uploads_log.txt`. The log file is pipe-separated and has the following columns:
`TIMESTAMP | SOURCE_IP | ENDPOINT | UPLOADED_FILENAME | EXPECTED_SHA256`

The upload application is hardcoded to save files to the base directory: `/home/user/app/uploads/`. 
However, an attacker may have used path traversal characters (`../`) in the `UPLOADED_FILENAME` to escape this directory and drop a file elsewhere on the system.

Your task is to write a Bash script (or execute a sequence of shell commands) that does the following:
1. Parses `/home/user/uploads_log.txt` to find the single log entry where the `UPLOADED_FILENAME` contains a path traversal attempt (i.e., contains `../`).
2. Computes the absolute path of where this file was actually written on the disk, assuming the application simply concatenated the base directory `/home/user/app/uploads/` and the `UPLOADED_FILENAME` without sanitization.
3. Computes the SHA256 checksum of the actual file on disk at that resolved path.
4. Compares the computed checksum of the file on disk against the `EXPECTED_SHA256` value recorded in the log entry.
5. Determines the octal permissions of the file on disk (e.g., 0644, 0777).

Finally, output your findings to a file named `/home/user/security_report.txt` in the exact format below:

```
Malicious File: <absolute_path_to_the_file_on_disk>
Hash Match: <Yes or No>
Permissions: <four_digit_octal_permissions>
```

Example of the expected format:
```
Malicious File: /home/user/app/malicious.php
Hash Match: Yes
Permissions: 0755
```