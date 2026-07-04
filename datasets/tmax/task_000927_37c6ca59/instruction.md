You are acting as a security auditor for a web application project. We suspect that some sandbox isolation mechanisms were breached due to misconfigured file permissions on scripts that process user uploads.

An intrusion detection system has generated an alert log located at `/home/user/ids_alerts.log`.

Your task is to write and execute a Python script (save it as `/home/user/remediate.py`) that performs the following actions:
1. Parse the log file `/home/user/ids_alerts.log`.
2. Find all file paths that are associated with the specific alert code `ALERT-SBX-09` (which indicates a sandbox escape attempt).
3. Check the file permissions of these specific flagged files. 
4. If a flagged file is world-writable (i.e., the "others" write bit is set), you must remove the world-writable permission (e.g., equivalent to `chmod o-w`). Do not alter other permissions (read/execute or user/group permissions).
5. Record the absolute paths of the files whose permissions you actually modified.
6. Output this list of modified files as a JSON array of strings to `/home/user/remediated_files.json`.

**Requirements:**
- The log format looks like this: `[2023-10-24 10:00:00] [ALERT-SBX-09] Suspicious activity in /home/user/project/script.py`
- Only modify files flagged with `ALERT-SBX-09`. Ignore other alerts (e.g., `ALERT-NET-01`).
- Only modify flagged files that are *currently* world-writable.
- The output file `/home/user/remediated_files.json` must be a valid JSON array, for example: `["/home/user/project/script.py"]`. If no files were modified, it should be an empty array `[]`.

The target files are all located in `/home/user/project/`. You have the necessary permissions to read the logs and modify these files.