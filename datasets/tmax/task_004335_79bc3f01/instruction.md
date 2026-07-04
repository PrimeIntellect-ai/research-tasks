You are acting as a DevSecOps engineer enforcing policy as code. 

We have an old authorization utility located at `/app/legacy_validator`. It is a compiled, stripped ELF binary that takes an authorization token as a command-line argument (e.g., `/app/legacy_validator <token>`). It exits with code `0` if the token is valid, and code `1` if it is invalid.

This legacy approach violates our security policy because command-line arguments are temporarily visible to other users on the system via `/proc`, leaking the sensitive token. We need to decommission the binary and replace it with a secure, network-based Python microservice.

Your task is to:
1. **Reverse Engineer the Oracle:** Analyze the `/app/legacy_validator` binary (e.g., using `strings`, `ltrace`, `strace`, or a decompiler) to discover the hardcoded secret token it accepts. 
2. **TLS/SSL Certificate Management:** Generate a self-signed RSA certificate (2048-bit) and private key. Save them as `/home/user/server.crt` and `/home/user/server.key`.
3. **Develop the Secure Service:** Write and run a Python HTTPS server (`/home/user/secure_auth_server.py`) that listens on `127.0.0.1:8443`.
    * The server must implement a `POST /auth` endpoint.
    * The endpoint must accept a JSON payload in the format: `{"token": "<string>"}`
    * If the provided token matches the secret token you extracted from the legacy binary, return an HTTP 200 OK status with the JSON response: `{"status": "success"}`.
    * If the token does not match (or is missing), return an HTTP 403 Forbidden status with the JSON response: `{"status": "forbidden"}`.
4. **Security Auditing/Logging:** The Python server must log every request to `/home/user/auth_audit.log`. Each log line must strictly follow this format:
   `[YYYY-MM-DD HH:MM:SS] IP_ADDRESS - Action: ALLOW` (if HTTP 200)
   `[YYYY-MM-DD HH:MM:SS] IP_ADDRESS - Action: DENY` (if HTTP 403)

Leave the Python service running in the background listening on port 8443. The automated testing suite will connect to your HTTPS service and issue real verification requests.