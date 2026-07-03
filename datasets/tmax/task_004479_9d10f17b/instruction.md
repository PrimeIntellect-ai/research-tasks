You are a penetration tester performing a security analysis on a legacy web application. You have been provided with a directory containing a compiled CGI binary and a web server access log. Your objective is to extract hardcoded vulnerable queries from the binary, identify attackers in the access log, redact sensitive information from their traces, and secure the binary's permissions.

The environment is located in `/home/user/pentest_target/`.
You have the following files:
1. `/home/user/pentest_target/cgi-bin/process_login` (An ELF executable used for handling logins)
2. `/home/user/pentest_target/logs/access.log` (The web server access log)

Perform the following tasks using standard bash CLI tools:

1. **Binary Analysis**: The `process_login` binary contains a hardcoded SQL query template used for authentication. Extract this exact SQL query string from the binary and save it to `/home/user/pentest_target/report/query_template.txt`. (Hint: It starts with `SELECT` and uses `%s` for string formatting).

2. **Injection Analysis & Sensitive Data Redaction**: Analyze the `access.log` to find all log entries where an attacker successfully exploited this login system using the classic SQL injection payload `admin' OR '1'='1` (URL encoded as `admin'%20OR%20'1'%3D'1` or similar, look for the literal decoded or encoded payload) that resulted in an HTTP 200 response code.
   For these specific attacker log lines *only*, redact the `SessionID` parameter value (e.g., `SessionID=abc123xyz`) by replacing the value with `REDACTED` (so it becomes `SessionID=REDACTED`). 
   Save these redacted log lines to `/home/user/pentest_target/report/attacker_logs_redacted.txt`.

3. **Access Control**: The `process_login` binary currently has overly permissive access. Change its permissions so that ONLY the owner has read, write, and execute permissions. No other users or groups should have any access.

Make sure the `report` directory exists before writing to it.