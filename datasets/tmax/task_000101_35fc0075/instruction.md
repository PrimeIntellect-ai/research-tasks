You are a DevSecOps engineer tasked with enforcing a new security policy. A local web service has been improperly logging sensitive HTTP headers and cookies in its JSON-formatted access logs. Additionally, the automated log backup system needs a hardened SSH configuration to securely transfer these logs.

Your task consists of two parts:

Part 1: Sensitive Data Redaction (Python)
There is a log file at `/home/user/raw_logs.jsonl`. Each line is a JSON object representing an HTTP request, containing a `headers` dictionary.
Write a Python script at `/home/user/redactor.py` and execute it to process this log file and write the sanitized output to `/home/user/redacted_logs.jsonl`.
The script must perform the following redactions on the `headers` dictionary:
1. If an `Authorization` header exists, replace its entire value with the exact string `[REDACTED]`.
2. If a `Cookie` header exists, inspect it for a `session_id` directive. Replace the value of the `session_id` with `[REDACTED]` (e.g., if the header is `theme=dark; session_id=abc123xyz; lang=en`, it should become `theme=dark; session_id=[REDACTED]; lang=en`). Other cookies in the string must remain unmodified.
3. The overall JSON structure and order of lines must be preserved.

Part 2: SSH Hardening and Key Management
The redacted logs will be pushed to a backup server. Ensure the local user's SSH setup is hardened for this automated transfer:
1. Generate an Ed25519 SSH keypair specifically for this backup without a passphrase. Save it to `/home/user/.ssh/log_backup_key`.
2. Create or modify the SSH client config file at `/home/user/.ssh/config` to include an entry for the host `backup.local`. For this host, strictly configure:
   - `PasswordAuthentication no`
   - `IdentityFile /home/user/.ssh/log_backup_key`

Ensure all specified output files (`/home/user/redacted_logs.jsonl`, the SSH keys, and the SSH config) are created with the exact requested paths and contents.