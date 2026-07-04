You are an incident responder investigating a suspected server breach. The web server access logs and a leaked fragment of the system's shadow file have been recovered. We believe the attacker cracked a specific user's password, authenticated via an API, and stole a session token.

Your investigation requires you to perform the following steps:

1. **Password Cracking**: Inspect `/home/user/shadow_leak.txt` to find the password hash for the user `admin_sys`. Use the provided dictionary file `/home/user/wordlist.txt` to crack this password. The system uses SHA-256 for password hashing (id `$5$`).
2. **HTTP Header & Log Inspection**: Analyze the web server logs in `/home/user/auth_events.json`. Each line is a JSON object representing an HTTP request/response. Find the successful login event for `admin_sys`. The API uses Basic Authentication, meaning the `Authorization` header in the request will contain `Basic ` followed by the Base64 encoded string of `username:password`.
3. **Session Correlation**: The successful login response sets a session cookie (found in the `response_headers` -> `Set-Cookie` field). Extract this `session_id`.
4. **Attacker Identification**: Extract the `ip_address` of the attacker who made the successful login request.

Finally, write your findings to a report file at `/home/user/investigation_report.txt` in the exact following format:
```
Password: <cracked_password>
Attacker IP: <ip_address>
Session ID: <session_id>
```

All required files (`/home/user/shadow_leak.txt`, `/home/user/wordlist.txt`, and `/home/user/auth_events.json`) are already present on the system. You may use any scripting language or command-line tools available to complete this task.