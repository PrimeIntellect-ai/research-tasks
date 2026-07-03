You are a compliance analyst preparing a mock vulnerable service for a red-team training exercise. You must build an "Audit Log Server" that simulates a legacy system with specific authentication flaws and data handling requirements.

Your tasks are to:

1. **Recover the Secret:** 
   Listen to the audio recording located at `/app/instructions.wav`. It contains spoken instructions from the senior analyst detailing how to recover the secret JWT key used by the legacy system. Follow the instructions precisely to recover the key. Any required files mentioned in the audio will be found in `/app/`.

2. **Generate TLS Certificates:**
   Generate a self-signed TLS/SSL certificate to secure the mock server. Save the certificate as `/home/user/cert.pem` and the private key as `/home/user/key.pem`.

3. **Develop the Audit Log Server:**
   Write a Python web server (using Flask, FastAPI, or the standard library) in `/home/user/server.py`.
   - The server must listen on `127.0.0.1:8443` over HTTPS using the generated certificates.
   - Implement a single endpoint: `POST /audit/log`.
   
4. **Authentication (Vulnerable JWT Implementation):**
   The endpoint must require a JWT in the `Authorization: Bearer <token>` header.
   - It must successfully validate tokens using the `HS256` algorithm signed with the secret key you recovered in Step 1.
   - **Vulnerability Injection:** To simulate the legacy flaw, the server MUST also bypass signature validation and accept the token if the JWT header specifies `"alg": "none"`.
   - It must return a `401 Unauthorized` status code for tokens with an invalid signature (where `alg` is not `none`).

5. **Sensitive Data Redaction:**
   Valid requests will contain a JSON payload with the following structure:
   `{"username": "<string>", "cc_number": "<string>", "event": "<string>"}`
   - You must redact the credit card number, replacing all digits except the last 4 with asterisks, in a dash-separated format (e.g., `1234567812345678` becomes `****-****-****-5678`). Assume input CC numbers are continuous 16-digit strings.
   - Append the audit log entry to `/home/user/audit.log` in exactly this format:
     `[<username>] <event> - <redacted_cc>`
   - Return a `200 OK` response if successful.

Run the server in the background so it is listening on port 8443 when your setup is complete. Do not hardcode the secret key in the script; have your script read it from `/home/user/jwt_secret.txt`, which you should create once you recover it.