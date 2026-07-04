You are acting as a compliance analyst for a corporate network. We have detected a potential insider threat and need you to generate a specific audit trail report by correlating access logs, leaked credentials, and system configurations.

You are provided with the following files in `/home/user/`:
1. `access.log`: An HTTP access log from our internal server.
2. `shadow_leak.txt`: A file containing leaked password hashes (username:sha256_hex_digest).
3. `wordlist.txt`: A dictionary of common corporate passwords.
4. `sudoers_audit.txt`: A backup of the `/etc/sudoers` file from the compromised internal machine.

Your task is to write a Python script that performs the following compliance checks:
1. **Security Log Parsing:** Analyze `access.log` to find the exact IP address that successfully accessed the sensitive endpoint `/admin/keys.zip` (HTTP status 200).
2. **Password Cracking:** Identify the user `audit_usr` in `shadow_leak.txt`. Using the provided `wordlist.txt`, write Python code to brute-force and find the plaintext password for this user. The hash is a standard SHA-256 hex digest of the password.
3. **Privilege Escalation Auditing:** Parse `sudoers_audit.txt` to determine the exact absolute path of the binary that `audit_usr` is permitted to execute as root without a password (e.g., `/usr/bin/nmap`).

Finally, your script must generate a JSON file at `/home/user/audit_report.json` with the exact following keys and your discovered values:
```json
{
  "attacker_ip": "<extracted_ip>",
  "cracked_password": "<plaintext_password>",
  "privesc_command": "<binary_path>"
}
```

Ensure your Python script creates the JSON file precisely formatted as requested. You may use standard Python libraries.