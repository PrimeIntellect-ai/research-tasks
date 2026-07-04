You are acting as an automated security auditing assistant. We have an audit report that needs to be securely served to our internal compliance network, but it must be properly redacted, secured with TLS, and protected by strict HTTP headers.

There is an image containing your instructions located at `/app/auditor_instructions.png`. Please extract the text from this image (you can use `tesseract` which is installed on the system). The image contains two key pieces of information:
1. A target username that must be redacted (format: `REDACT_USER: <username>`).
2. A mandatory authentication token (format: `AUTH_TOKEN: <token>`).

Your task is to implement and start a secure HTTPS server in Python that fulfills the following requirements:

1. **TLS/SSL Setup**: 
   - Generate a self-signed certificate (`cert.pem`) and private key (`key.pem`) valid for `localhost`.
   - Place these files in `/home/user/certs/`.

2. **Secure HTTPS Server**:
   - Write and run a Python script that starts an HTTPS web server listening exactly on `127.0.0.1:8443`.
   - The server must handle `GET` requests to the `/audit-report` endpoint.

3. **Authentication**:
   - The server must check for the `Authorization` header.
   - It must only accept the exact Bearer token extracted from the image (e.g., `Authorization: Bearer <token>`).
   - Requests without the correct token must receive an HTTP 401 Unauthorized response.

4. **Sensitive Data Redaction**:
   - Read the raw log file located at `/home/user/audit_logs.txt`.
   - Before serving the content, you must replace all occurrences of the extracted `<username>` with the exact string `[REDACTED]`.

5. **Content Security Policy Enforcement**:
   - The successful HTTP 200 response must include the following header exactly:
     `Content-Security-Policy: default-src 'self'; frame-ancestors 'none';`
   - The response body should be the redacted audit log text (Content-Type: text/plain).

Keep the server running in the foreground or background so that our automated verifier can connect to `https://127.0.0.1:8443/audit-report` and validate the redaction, the CSP headers, and the TLS configuration.