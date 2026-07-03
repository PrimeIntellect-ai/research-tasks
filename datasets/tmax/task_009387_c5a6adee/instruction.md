You are a compliance analyst generating an audit trail for a legacy internal application. You need to verify its integrity, demonstrate a known open redirect vulnerability, and establish a hardened SSH configuration for secure log delivery. 

Perform the following tasks:

1. **File Integrity Verification:**
   The source code for the application is located at `/home/user/app/server.py`. The known good baseline SHA256 hash is stored in `/home/user/compliance/baseline.sha256`. 
   Calculate the SHA256 hash of `/home/user/app/server.py`. Compare it to the baseline.
   Create an audit report file at `/home/user/audit_report.txt`. 
   On the first line of this file, write exactly `Integrity: MATCH` if the hashes match, or `Integrity: MISMATCH` if they do not.

2. **Exploit Crafting (Open Redirect):**
   The application is running locally on `http://127.0.0.1:8080`. The login endpoint at `/login` accepts a `url` query parameter for redirection after a successful login. However, it suffers from an open redirect vulnerability that carelessly appends a sensitive session token to the redirected URL.
   Craft a Bash script at `/home/user/exploit.sh` that uses `curl` to exploit this vulnerability. You must construct a request to the `/login` endpoint that forces the server to issue a 302 redirect to `http://127.0.0.1:9090/audit_catcher`. 
   Capture the `Location` header from the server's HTTP response, extract the value of the `token` parameter appended to your provided URL, and append it to your audit report.
   On the second line of `/home/user/audit_report.txt`, write exactly `Token: <EXTRACTED_TOKEN_VALUE>` (replace `<EXTRACTED_TOKEN_VALUE>` with the actual token you extracted).

3. **SSH Hardening and Key Management:**
   To securely transmit this audit report later, you need to configure a hardened SSH profile.
   - Generate a new SSH key pair of type `ed25519` with no passphrase. Save the private key to `/home/user/.ssh/compliance_key`.
   - Create or modify the SSH configuration file at `/home/user/.ssh/config`.
   - Add a configuration block for a Host named `audit-vault`.
   - Set the `Hostname` for this block to `127.0.0.1`.
   - Set the `IdentityFile` to `/home/user/.ssh/compliance_key`.
   - Restrict the `Ciphers` to only `chacha20-poly1305@openssh.com`.
   - Restrict the `MACs` to only `hmac-sha2-512-etm@openssh.com`.
   
   Finally, append the generated public key (the exact contents of `/home/user/.ssh/compliance_key.pub`) to the third line of your audit report. Write exactly `PubKey: <PUBLIC_KEY_CONTENTS>` on the third line of `/home/user/audit_report.txt`.

Ensure `/home/user/audit_report.txt` has exactly three lines formatted as specified above.