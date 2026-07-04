You are acting as a security engineer who is rotating credentials after a suspected session hijacking incident. The incident is believed to have been caused by an open redirect vulnerability in the login flow.

You have been provided with a directory of raw HTTP response headers captured by a reverse proxy. These logs are located in `/home/user/http_logs/`.

Your task is to:
1. Audit the HTTP logs to identify the single file that demonstrates an open redirect vulnerability. The application's legitimate domain is `https://internal-app.local`. Any redirect (`Location:` header) pointing to a different domain indicates the vulnerable response.
2. Extract the compromised session token. Find the `Set-Cookie` header in the vulnerable log file and extract the value of the `session_id` cookie.
3. Verify the integrity of the new credential file before rotation. Check the SHA-256 hash of `/home/user/new_keys.pem` against the expected hash found in `/home/user/keys.checksum`.
4. Create an incident report at `/home/user/incident_report.txt` with the following exact format:

```
Vulnerable_File: <filename>
Leaked_Session: <session_id_value>
Keys_Intact: <true or false>
```

For example, if the vulnerable file was `req_99.txt`, the session id was `deadbeef`, and the checksums matched (so keys are intact), the file should look exactly like:
```
Vulnerable_File: req_99.txt
Leaked_Session: deadbeef
Keys_Intact: true
```

Ensure all findings are accurate and the report format exactly matches the specification. You are expected to use standard bash command-line tools (grep, awk, sha256sum, etc.) to complete this task.