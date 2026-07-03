You are acting as a compliance analyst for a web company. You need to generate an audit trail report based on a recent server log dump and system configuration files.

All files are located in `/home/user/audit_trail/`. 

Here is your task:
1. **Decryption**: You have been provided with an encrypted symmetric key file (`/home/user/audit_trail/symmetric.enc`) and an RSA private key (`/home/user/audit_trail/private.pem`). The symmetric key was encrypted using RSA PKCS#1 v1.5. Decrypt it to reveal a base64-encoded Fernet key.
2. **Log Analysis**: Use the decrypted Fernet key to decrypt the log file (`/home/user/audit_trail/logs.enc`). The decrypted logs are in JSON Lines format (one JSON object per line), representing HTTP request payloads.
3. **Vulnerability Categorization**: Analyze the decrypted logs to identify potential attacks in the `payload` field:
   - **SQL Injection (SQLi)**: Count any log entry where the payload contains the exact substring `' OR '1'='1` or `UNION SELECT`.
   - **Cross-Site Scripting (XSS)**: Count any log entry where the payload contains the exact substring `<script>`.
4. **Privilege Escalation Audit**: Review the backup of the system's sudoers file at `/home/user/audit_trail/sudoers_backup`. Identify any active (uncommented) users who have been granted `NOPASSWD: ALL` privileges. Ignore the `root` user.
5. **Reporting**: Generate a JSON report at `/home/user/audit_trail/compliance_report.json` with the following exact structure:
```json
{
  "sql_injection_count": 0,
  "xss_count": 0,
  "critical_sudo_users": ["username1", "username2"]
}
```
Replace the integers and array with your actual findings. Sort the `critical_sudo_users` array alphabetically.

You must use Python to perform the decryption and parsing tasks. Shell commands can be used to set up the environment or run your scripts.