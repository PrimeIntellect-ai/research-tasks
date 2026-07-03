You are acting as a network security engineer investigating a recent incident. We suspect an attacker exploited a path traversal vulnerability in our file upload handler and we need to identify compromised user accounts.

You are provided with:
1. A web server log file located at `/home/user/server.log`. Each line is a JSON object representing an HTTP request.
2. The server's secret key for signing session tokens, located at `/home/user/secret.key`.

Your task is to write a Python script (using only standard libraries) at `/home/user/analyze.py` that processes the log file and identifies successful, authenticated path traversal attacks.

The script must perform the following:
1. **Log Parsing:** Read `/home/user/server.log` line by line. Each line contains `timestamp`, `ip`, `method`, `path`, and `headers` (a dictionary).
2. **Intrusion Detection:** Identify requests where the `path` OR the `headers["X-Upload-Path"]` contains a path traversal sequence. You must match exactly the sequences `../`, `..\`, or their URL-encoded forms `%2e%2e%2f` and `%2e%2e%5c` (case-insensitive).
3. **Cookie Inspection:** For each malicious request, extract the `session` token from the `Cookie` header (e.g., `Cookie: session=TOKEN; other=value`).
4. **Token Validation:** The session token has the format `PAYLOAD.SIGNATURE`.
    - `PAYLOAD` is a base64url-encoded JSON string containing a `username` field.
    - `SIGNATURE` is a base64url-encoded HMAC-SHA256 hash of the `PAYLOAD` string, using the secret key from `/home/user/secret.key`.
    - Validate the signature of the token. Ignore the request if the signature is invalid or missing.
5. **Output:** For every malicious request with a *valid* session token, write a line to `/home/user/compromised_users.txt` in the exact format:
   `IP,username`
   (e.g., `192.168.1.5,admin`). If a user/IP combination appears multiple times, write it each time it occurs.

Requirements:
- Ensure your Python script is executable and run it to generate the final `/home/user/compromised_users.txt` file.
- Do not use any external Python packages (like `requests` or `jwt`); use only the standard library (`json`, `base64`, `hmac`, `hashlib`, `re`, etc.).
- Note that base64url encoding omits padding (`=`), so your script should add appropriate padding before decoding if necessary.