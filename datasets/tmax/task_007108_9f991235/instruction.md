You are acting as a security auditor. We have discovered that a recent deployment of our custom web server contained a flawed permission checking mechanism that resulted in an open redirect vulnerability in the login flow. Attackers have exploited this to redirect users to malicious external domains after a successful login.

Your task is to analyze the web server's access logs, identify the successful open redirect exploits, and generate a redacted report of the compromised sessions.

The logs are located at `/home/user/audit_data/access.log`.
The log format is a custom combined format:
`IP_ADDRESS - - [DATE] "METHOD PATH_WITH_QUERY HTTP_VERSION" STATUS_CODE RESPONSE_SIZE "session_id=TOKEN"`

A normal login redirect looks like this:
`192.168.1.15 - - [20/Nov/2023:14:01:00 +0000] "GET /login?redirect=/dashboard HTTP/1.1" 302 512 "session_id=a1b2c3d4"`

An exploited open redirect occurs when the `redirect` parameter contains an absolute URL starting with `http://` or `https://` AND the server responds with an HTTP status code `302`. (If the server responds with `403` or `400`, the exploit was blocked and should not be included).

Write a Bash script at `/home/user/analyze_redirects.sh` that performs the following:
1. Parses `/home/user/audit_data/access.log`.
2. Identifies all lines representing a successful open redirect exploit (HTTP 302 with an external URL in the `redirect` parameter).
3. Redacts the sensitive data in those specific log lines:
   - Replace the first three octets of the IPv4 address with `***.***.***.` (e.g., `10.5.22.100` becomes `***.***.***.100`).
   - Replace the session token value with `REDACTED` (e.g., `"session_id=a1b2c3d4"` becomes `"session_id=REDACTED"`).
4. Outputs the findings to a file named `/home/user/compromised_sessions.txt`.

The format of `/home/user/compromised_sessions.txt` must be one line per compromised session, formatted exactly as follows:
`[EXTRACTED_MALICIOUS_URL] REDACTED_LOG_LINE`

Example output line:
`[http://evil.com/steal] ***.***.***.15 - - [20/Nov/2023:14:05:00 +0000] "GET /login?redirect=http://evil.com/steal HTTP/1.1" 302 512 "session_id=REDACTED"`

Ensure your script is executable and run it to generate the final `compromised_sessions.txt` file.