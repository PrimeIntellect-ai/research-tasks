You are an incident responder analyzing a suspected evasion tool used in a recent simulated red-team exercise. We have recovered a stripped executable located at `/app/evasion_sim`. Preliminary analysis suggests this tool attempts to exploit insecure JWT implementations by stripping the signature algorithm (`alg: none`) to bypass authentication and gain unauthorized privilege escalation.

Your task is to build an active Python-based honeypot service to safely interact with this tool, capture its payloads, and log its evasion attempts for further security correlation.

Follow these specific instructions:

1. **Certificate Management:** Generate a self-signed TLS/SSL certificate and private key. Place them at `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`. 
2. **Service Setup:** Create and run a Python HTTPS web server listening securely on `127.0.0.1:9090`. It must serve traffic using the generated TLS certificates.
3. **Vulnerability Emulation & Logging:** 
   - The service must expose a `POST /auth` endpoint.
   - When a request is received, extract the raw JWT from the `Authorization: Bearer <token>` header.
   - Calculate the SHA-256 checksum of the raw JWT string.
   - Decode the JWT payload (ignoring signature validation for the purpose of this honeypot). 
   - Check if the header contains `"alg": "none"` (case-insensitive) and the payload contains `"role": "admin"`.
   - If this evasion pattern is detected, append a log entry to `/home/user/security_logs.txt` in the exact format:
     `ALERT: Evasion attempt detected | Hash: <sha256_checksum> | Escaping to role: admin`
4. **Privilege Escalation Audit:** If the evasion pattern is detected, the server must also check the effective user ID (UID) of the running Python process. Append to `/home/user/privesc_audit.log` either `SAFE: running as unprivileged user` (if UID != 0) or `CRITICAL: running as root` (if UID == 0).
5. **Response:** The server should return an HTTP 200 OK with JSON `{"status": "logged"}` to keep the simulated attacker engaged.

Ensure the server runs in the background or is actively running so our automated test suite can connect to it, send simulated payloads, and verify your logging logic. You may use standard Python libraries (e.g., `http.server`, `ssl`, `json`, `hashlib`, `base64`, `os`).