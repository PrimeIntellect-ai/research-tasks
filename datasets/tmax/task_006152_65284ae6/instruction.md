You are acting as a security auditor and developer for a small internal service. A recent security audit revealed that the file upload service located at `/home/user/app/upload_server.go` contains a severe path traversal vulnerability. An attacker has already exploited this to upload a rogue public key to the system, granting themselves unauthorized SSH access and escalating their privileges.

Your objectives are to remediate the vulnerability, secure the server with Mutual TLS (mTLS), and clean up the compromised state.

Complete the following steps:

1. **Privilege Escalation Audit & Cleanup:**
   Inspect `/home/user/.ssh/authorized_keys`. You will find a legitimate key (comment: `legitimate@admin`) and a rogue key uploaded by the attacker (comment: `hacker@evil`). 
   Remove ONLY the rogue key from the `authorized_keys` file to revoke the attacker's access. Do not alter the legitimate key.

2. **Fix Path Traversal:**
   The Go application currently accepts file uploads via a `POST` request to `/upload?filename=<name>`. 
   Modify `/home/user/app/upload_server.go` to prevent path traversal. The server must safely restrict all uploaded files to strictly reside within the `/home/user/app/uploads/` directory. If a path traversal attempt is detected (e.g., using `../`), the server should return an HTTP 400 Bad Request status code.

3. **Certificate Management (mTLS):**
   The server currently runs in plaintext HTTP on port 8080. You must secure it.
   Create a directory `/home/user/certs/` and generate the following using `openssl`:
   - A Root CA certificate and key (`ca.crt`, `ca.key`).
   - A Server certificate and key (`server.crt`, `server.key`), signed by your Root CA, valid for `localhost`.
   - A Client certificate and key (`client.crt`, `client.key`), signed by your Root CA.

4. **Network Policy & Server Hardening:**
   Update `/home/user/app/upload_server.go` to run as an HTTPS server on port `8443` (instead of 8080).
   Configure the server to require and validate client certificates (Mutual TLS) using your Root CA (`ca.crt`). The server must reject requests that do not present a valid client certificate signed by your CA.

5. **Finalization:**
   Compile the fixed server to `/home/user/app/upload_server` and leave it running in the background.
   Create a file `/home/user/audit_report.txt` containing exactly the string: `Vulnerability fixed and mTLS enabled`.

Ensure that your compiled Go server is actively listening on port 8443 before you finish.