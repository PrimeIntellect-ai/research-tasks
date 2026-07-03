You are a security engineer performing a post-incident credential rotation and log sanitization. An external Incident Response (IR) team needs to analyze your SSH authentication logs, but you must redact sensitive information—specifically, instances where users accidentally typed their passwords or emails into the username prompt, as well as attempts to brute-force the `root` account. 

Your task consists of two parts: Log Redaction (using Go) and Key Rotation (using Shell).

**Part 1: Log Redaction**
An SSH authentication log is located at `/home/user/auth.log`.
Write a Go script at `/home/user/process_logs.go` that reads this file and writes a sanitized version to `/home/user/redacted_auth.log`.

The script must implement the following pattern matching and redaction logic:
1. Identify lines containing SSH login failures. Specifically, look for lines containing `Failed password for invalid user <USERNAME> `, `Failed password for <USERNAME> `, or `Invalid user <USERNAME> `.
2. Check if the `<USERNAME>` matches any of our sensitive criteria:
   - The username contains an `@` symbol (likely an email address).
   - The username is exactly `root`.
3. If the username matches the sensitive criteria, replace the `<USERNAME>` string in that log line with the exact string `[REDACTED]`.
4. All other lines (and failed logins with non-sensitive usernames) must be written to the output file exactly as they appear in the original log.
5. Compile and run your Go script so that `/home/user/redacted_auth.log` is generated.

**Part 2: Key Rotation**
Because of the suspicious activity, you must rotate the credentials for the local user. 
Using standard shell commands, generate a new Ed25519 SSH keypair.
- The private key must be saved exactly to `/home/user/.ssh/id_ed25519_rotated`
- The key must have an empty passphrase.
- Do not modify any existing keys in the `~/.ssh/` directory.

Ensure both parts are complete and the `redacted_auth.log` file is fully written before you finish.