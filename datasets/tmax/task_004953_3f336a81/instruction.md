You are a security auditor tasked with investigating a potential security breach and auditing system backups for permission misconfigurations. You will write a Python script to parse security logs and analyze file permissions, combining intrusion detection pattern matching with SSH key management auditing.

Your objectives:

1. **Intrusion Pattern Matching (Log Parsing)**
You have been provided with an SSH log file at `/home/user/server_logs/auth.log`.
Write a Python script that parses this log file to find a specific intrusion pattern:
Find all unique IP addresses that generated exactly three (3) consecutive "Failed publickey" log entries for the user "admin", followed immediately by an "Accepted publickey" entry for the user "admin" from the same IP address. "Immediately" means there must be no other log entries for that specific IP address between the 3 failures and the 1 success.

2. **SSH Hardening & Permission Auditing**
You have been provided with a backup of user directories at `/home/user/home_backup/`.
Your Python script must recursively audit this directory to find:
- **Vulnerable Private Keys:** Any file containing the exact string `-----BEGIN OPENSSH PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----` anywhere in its content, which has file permissions that are broader than `600` (e.g., if group or others have read, write, or execute permissions).
- **Vulnerable SSH Directories:** Any directory named exactly `.ssh` that has permissions broader than `700`.

3. **Reporting**
Your script must be saved as `/home/user/generate_report.py`. When run, it should generate a JSON report file at `/home/user/audit_report.json` with the following exact structure:

```json
{
  "compromised_ips": ["<IP1>", "<IP2>"],
  "vulnerable_keys": ["<absolute_path_to_key1>", "<absolute_path_to_key2>"],
  "vulnerable_ssh_dirs": ["<absolute_path_to_dir1>"]
}
```

Constraints:
- The lists in the JSON output should be sorted in ascending alphabetical/lexicographical order.
- Use absolute paths in the `vulnerable_keys` and `vulnerable_ssh_dirs` lists.
- You must use Python to perform the file reading, permission checking (using `os.stat`), and JSON generation.
- The `generate_report.py` script should be executable or runnable via `python3 /home/user/generate_report.py`.