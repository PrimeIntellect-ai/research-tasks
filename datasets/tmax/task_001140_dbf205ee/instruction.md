As a compliance analyst, you are tasked with securing a legacy audit trail system. We have a vendored package called `bash-web-auditor` (version 1.0) located at `/app/bash-web-auditor`. It provides a simple Bash-based HTTP API, but it has several security and build issues. 

Please perform the following steps to fix and deploy the system securely:

1. **Fix the Build**: The `Makefile` in `/app/bash-web-auditor` is broken due to a typo in the `install` target. Fix the Makefile so that running `make install` successfully copies `auditor.sh` and `worker.sh` to `/home/user/bin/` and makes them executable.
2. **Sensitive Data Redaction**: The `auditor.sh` script reads an HTTP request, extracts the Bearer token from the `Authorization` header, and writes it directly to `/app/audit.log`. Modify the installed `/home/user/bin/auditor.sh` so that it redacts the token in the log file (replace the actual token string with the exact string `[REDACTED]`).
3. **Prevent Command-Line Exposure**: `auditor.sh` currently spawns `worker.sh` and passes the extracted token as a command-line argument, which leaks the credential to any user via `/proc`. Modify `auditor.sh` to pass the token to `worker.sh` via an environment variable named `SECRET_TOKEN` instead, and remove the command-line argument. (You do not need to modify `worker.sh`).
4. **CWE Identification**: Identify the standard Common Weakness Enumeration (CWE) identifier for "Insertion of Sensitive Information into Log File". Write the exact ID (e.g., `CWE-123`) to `/app/cwe.txt`.
5. **Certificate Chain Setup**: We must serve this API over HTTPS. Generate a new local Root CA certificate and a server certificate for `localhost` signed by this Root CA. 
   - Save the Root CA certificate to `/app/ca.crt`.
   - Save the server certificate to `/app/server.crt`.
   - Save the server private key to `/app/server.key`.
   (Use RSA 2048-bit keys and ensure the certificates are valid for at least 30 days).
6. **Deploy the Service**: Start the fixed `/home/user/bin/auditor.sh` as an HTTPS server listening on `127.0.0.1:8443`. You must use `socat` to wrap the script in an SSL listener using the server certificate and key you generated. The service must run in the background and remain active for testing. Make sure `socat` correctly executes the script for each incoming connection.

Ensure your background service is running when you complete the task. An automated verifier will make an HTTPS request to `https://127.0.0.1:8443/` using your `/app/ca.crt` to validate the certificate chain, and it will check `/app/audit.log` for proper redaction.