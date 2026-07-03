You are acting as a security auditor for a legacy web application. The application currently dumps raw authentication logs into a directory with overly permissive access rights, potentially leaking sensitive user session tokens. 

Your objective is to identify, redact, and securely store these logs to prevent unauthorized access to the tokens, while generating an audit summary.

Here are your specific instructions:

1. **Locate and Analyze**: The raw logs are located in `/home/user/app_logs/`. These files end in `.log`. Inspect them to understand their structure. 
2. **Redact Sensitive Data**: Write a Python script at `/home/user/redact_logs.py` that reads all `.log` files in `/home/user/app_logs/`. The script must identify any sensitive tokens using pattern matching. Tokens appear strictly in the format `Token: <alphanumeric_string>` (e.g., `Token: A1b2C3d4`). The script must replace the `<alphanumeric_string>` portion with `[REDACTED]`, resulting in `Token: [REDACTED]`.
3. **Secure Storage**: The Python script should save the redacted versions of the logs into a new directory: `/home/user/secure_audit/`. The redacted files must have the exact same names as their originals.
4. **Fix Permissions**: To simulate proper process isolation and secure storage, ensure that the new directory `/home/user/secure_audit/` has `700` permissions (read/write/execute for the owner only), and all redacted `.log` files inside it have exactly `600` permissions (read/write for the owner only).
5. **Audit Report**: Generate a final summary report at `/home/user/audit_report.txt`. This file must contain exactly one line with the total number of tokens redacted across all files, in this exact format:
   `Total Redactions: <number>`

Run your script and ensure all files, directories, permissions, and the audit report are correctly established.