You are acting as an incident responder investigating a compromised file upload service. The attacker exploited a path traversal vulnerability in a custom C binary and left behind a ransom note image. You need to analyze the artifacts, redact leaked sensitive data, and spin up a secure honeypot service using Bash to monitor further attacks.

Here are your investigation steps:

1. **Extract Information from the Ransom Note:**
   The attacker left an image at `/app/ransom.png`. Use OCR (e.g., `tesseract`) to read the text in this image. The image contains a message specifying a 4-digit port number the attacker wants you to communicate on. Note this port number.

2. **Reverse Engineer the Vulnerable Binary:**
   Analyze the compiled binary located at `/app/upload_handler.bin`. The binary contains a hardcoded absolute directory path where it was supposed to store uploaded files before the path traversal occurred. Find this hardcoded upload directory path and write it exactly as found into `/app/vuln_dir.txt`.

3. **Log Redaction:**
   The attacker downloaded logs containing sensitive session cookies. A copy of the recovered logs is at `/app/compromised_logs.txt`. 
   Write a Bash script to parse this file and replace the value of any session token found in the `Cookie` header (specifically the format `session_token=<alphanumeric_string>`) with the exact string `[REDACTED]`. Save the cleaned log to `/app/clean_logs.txt`.

4. **Deploy a Bash-based Secure Honeypot Service:**
   Using Bash (and tools like `nc` or `socat`), create and run a lightweight HTTP server listening on `127.0.0.1` at the 4-digit port you extracted from the ransom image in Step 1.
   
   Your Bash server must:
   - Run continuously and handle incoming HTTP GET requests.
   - If the request line exactly matches `GET /logs HTTP/1.1`, respond with a valid HTTP `200 OK` response containing the contents of `/app/clean_logs.txt` as the body.
   - Defend against path traversal: If the requested URI contains `..` (e.g., `GET /../../etc/passwd HTTP/1.1`), it must immediately respond with `HTTP/1.1 403 Forbidden` and no body.
   - Include the custom HTTP header `X-Incident-Response: Active` in ALL responses.
   - For any other path, return `HTTP/1.1 404 Not Found`.

Keep your honeypot server running in the background or foreground so that our automated systems can test it.