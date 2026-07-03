You are an incident responder investigating a suspected breach on a web server. The server has an application that accepts file uploads, and we believe it is susceptible to path traversal. 

You have been provided with the following evidence:
1. The web server access logs located at `/home/user/logs/web.log`. This log includes HTTP methods, URLs, status codes, and HTTP headers (including Cookies).
2. A directory where we suspect a file was dropped outside the intended upload directory: `/home/user/compromised/`.

Your objective is to write a Python script (or use a combination of Python and shell commands) to analyze the logs and perform the following tasks:
1. **Identify the Attacker:** Find the IP address that successfully exploited a path traversal vulnerability on the `/upload` endpoint (indicated by `../` patterns in the URL and a `200` HTTP status code).
2. **Session Hijacking:** Extract the `session` cookie value used by this attacker IP during their successful upload request.
3. **Payload Hashing:** The attacker used the path traversal to drop a file in the `/home/user/compromised/` directory. Locate this file on the filesystem based on the filename specified in the successful traversal log entry. Calculate the SHA256 hash of this malicious file.
4. **Vulnerability Analysis:** Scan the logs for all requests made by the attacker IP and count how many of them contained Cross-Site Scripting (XSS) payloads in the URL (specifically, look for the exact case-insensitive strings `<script>` or `javascript:`).
5. **Quarantine:** Change the file permissions of the dropped malicious file to `000` to prevent execution.

Output your final findings to a JSON file at `/home/user/incident_report.json` with the following exact keys and types:
- `"attacker_ip"` (string)
- `"session_cookie"` (string - just the value of the session cookie)
- `"malicious_file_hash"` (string - lowercase hex digest of the SHA256 hash)
- `"xss_attempt_count"` (integer - number of requests from the attacker IP containing the specified XSS patterns)

Ensure your output strictly adheres to this JSON structure.