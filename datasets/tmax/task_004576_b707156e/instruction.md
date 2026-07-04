You are a security engineer assigned to perform a critical credential rotation and security remediation for an internal multi-service application. The system is located in `/app/` and consists of a Go-based API gateway, a Go-based data backend, and a legacy compiled utility. 

Your objective is to patch vulnerabilities, enforce security headers, reverse-engineer a legacy key, rotate the encryption keys, and bring the services online.

Here is the current state of `/app/`:
- `/app/gateway/main.go`: The public-facing HTTP gateway.
- `/app/backend/main.go`: The internal backend service that processes sensitive data.
- `/app/legacy_bin/vault_extractor`: An unstripped, legacy ELF binary used by the old system.
- `/app/logs/`: Directory for application logs.

Perform the following tasks:

1. **Reverse Engineering:** The old encryption system used a 32-byte AES key hardcoded inside the `/app/legacy_bin/vault_extractor` binary. It is stored as a plaintext string prefixed with `AES_KEY_`. Reverse engineer or inspect the binary to extract this old key.

2. **Sensitive Data Redaction (CWE-532):** The backend service (`/app/backend/main.go`) contains an Information Exposure vulnerability. It blindly logs incoming JSON requests to `/app/logs/backend.log`. You must audit the code and modify it so that the value of the `user_token` field in any incoming JSON payload is replaced with the exact string `[REDACTED]` before being written to the log file. 

3. **Encryption & Credential Rotation:** 
   - The backend service currently uses the old key (which you must replace).
   - Modify `/app/backend/main.go` to accept a new 32-byte encryption key via the `NEW_MASTER_KEY` environment variable.
   - The backend exposes a `POST /process` endpoint. It receives JSON: `{"user_token": "...", "data": "..."}`. You must ensure the backend encrypts the value of the `data` field using AES-GCM with the `NEW_MASTER_KEY`, hex-encodes the ciphertext (appending the nonce properly so it can be decrypted, standard format `hex(nonce + ciphertext)`), and returns it as `{"encrypted_data": "<hex_string>"}`.

4. **CSP Enforcement:** The API gateway (`/app/gateway/main.go`) exposes a `POST /api/v1/data` endpoint that forwards requests to the backend. Modify the gateway to enforce a strict Content Security Policy. Every response from the gateway must include the HTTP header:
   `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';`

5. **Service Composition & Startup:**
   - Compile both Go services.
   - Set the `NEW_MASTER_KEY` environment variable to `f4a8b2c9d3e7f1a5b6c0d4e8f2a9b3c7`.
   - Start the backend service so it listens on `127.0.0.1:9090`.
   - Start the gateway service so it listens on `127.0.0.1:8080`.
   - Ensure both processes remain running in the background.

Do not write any wrapper scripts that intercept the network traffic; modify the actual Go source code. When you are finished, leave the services running. An automated verifier will send protocol-level requests to test the end-to-end flow.