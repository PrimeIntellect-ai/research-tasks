You are acting as a compliance analyst investigating a legacy file upload handler suspected of processing path traversal attacks. You have been provided with an intercepted log of upload events and need to generate a secure audit trail.

You have the following files in your environment:
1. `/home/user/upload_logs.txt`: A log file where each line represents an upload event in the format `TOKEN | ENCODED_FILENAME`.
2. `/home/user/secret.key`: A file containing the secret key used to sign the tokens.

**Task Requirements:**
1. Read and parse `/home/user/upload_logs.txt`.
2. For each line, decode the `ENCODED_FILENAME` (which is Base64 encoded).
3. Check if the decoded filename is malicious by matching it against path traversal patterns. Specifically, flag the filename if it contains the exact string `../` or the URL-encoded equivalent `..%2f` (case-insensitive).
4. If the filename is **not** malicious, ignore the line and move to the next.
5. If the filename **is** malicious, evaluate the `TOKEN`. 
   - The token format is `<base64_url_safe_no_padding_payload>.<base64_url_safe_no_padding_mac>`.
   - The payload, when base64url-decoded, is a JSON object containing at least a `"user"` key (e.g., `{"user": "alice"}`).
   - The MAC is an HMAC-SHA256 signature of the raw base64-encoded payload string (the part before the dot), signed using the raw text inside `/home/user/secret.key`.
6. Verify the token's MAC. 
7. Generate an audit trail and save it to `/home/user/audit_trail.json`. The file must contain a single JSON array of objects, preserving the original order of the malicious logs. Each object must have the following exact schema:
   - `"user"`: The string value extracted from the token's payload.
   - `"malicious_payload"`: The decoded malicious filename (string).
   - `"signature_valid"`: A boolean indicating whether the HMAC-SHA256 signature matched.

Write and execute a Python script to perform this analysis.