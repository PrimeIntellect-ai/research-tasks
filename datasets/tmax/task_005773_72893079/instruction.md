You are a security engineer tasked with rotating credentials and hardening a legacy internal Python API service. The service is currently running with outdated credentials and lacks proper security headers and network binding policies.

The web service is located at `/home/user/app.py`. 
Currently, it binds to all interfaces (`0.0.0.0`), uses an old TLS certificate (`/home/user/old_cert.pem`), and expects an outdated API token (`OLD_SUPER_SECRET`).

Perform the following tasks to secure the application:

1. **TLS Certificate Management**: 
   Generate a new RSA 2048-bit self-signed certificate and private key. Save them exactly as `/home/user/new_cert.pem` and `/home/user/new_key.pem`. Set the Common Name (CN) to `localhost`.

2. **Network Policy & Secure Coding**: 
   Modify `/home/user/app.py` to implement the following security upgrades:
   - Change the bind address from `0.0.0.0` to `127.0.0.1` so the service is only accessible locally.
   - Update the `ssl_context` to use your newly generated `new_cert.pem` and `new_key.pem`.
   - Update the expected Bearer token in the authentication logic to `NEW_ROTATED_TOKEN_2024`.
   - Implement Content Security Policy (CSP) enforcement. Add the HTTP header `Content-Security-Policy: default-src 'self';` to the successful JSON response in the `/data` route.

3. **Authentication Flow Testing**: 
   Start your modified Flask application in the background (e.g., `python3 /home/user/app.py &`). Wait a few seconds for it to start.
   
   Create a bash script at `/home/user/verify.sh` that uses `curl` to test the updated authentication flow and network policy. Your script should:
   - Make an HTTPS GET request to `https://127.0.0.1:8443/data`.
   - Ignore self-signed certificate warnings.
   - Pass the new authentication token correctly in the `Authorization` header.
   - Extract the HTTP Status Code, the `Content-Security-Policy` header value, and the raw JSON response body.
   - Write these values to an audit log file at `/home/user/audit_log.txt` in the exact following format:

```text
Status: <HTTP_STATUS_CODE>
CSP: <CSP_HEADER_VALUE>
Body: <RAW_JSON_BODY>
```
*(Example: `Status: 200`, `CSP: default-src 'self';`, `Body: {"data":"secure sensitive data"}`)*

Finally, execute your `/home/user/verify.sh` script to produce the `/home/user/audit_log.txt` file. Make sure the log file is generated successfully before finishing.