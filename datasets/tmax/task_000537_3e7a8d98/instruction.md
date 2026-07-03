You are an incident responder investigating a compromised Linux server. The server hosts a file upload service that was recently breached. We suspect the attacker exploited a path traversal vulnerability to drop a persistent backdoor, manipulate our authentication tokens, and tamper with our internal certificate chain. 

Your objective is to investigate the breach, identify the attacker's actions, reverse-engineer their backdoor authentication, and prepare remediation steps.

Perform the following tasks:

1. **Log Analysis & Correlation:**
   Examine the web server log located at `/home/user/investigation/access.log`. Identify the IP address of the attacker and the exact path traversal payload they used in the `path` parameter during a successful `POST /upload` request (HTTP 200). 
   Create a JSON report at `/home/user/incident_report.json` with exactly two keys:
   - `"attacker_ip"`: The identified IP address.
   - `"traversal_payload"`: The exact string used in the path parameter.

2. **Cryptanalysis & Token Forgery:**
   The attacker left behind a custom authentication service script at `/home/user/investigation/auth_service.py`. This script contains a weak proprietary token generation algorithm. Analyze the Python code to understand the token generation logic. 
   Using this logic, forge a valid authentication token for the username `"system_admin"`. Write this forged token (just the raw token string) to `/home/user/admin_token.txt`.

3. **Certificate Chain Validation:**
   The directory `/home/user/investigation/certs/` contains a root CA (`rootCA.pem`) and several intermediate/leaf certificates. The attacker has planted a rogue, forged certificate in this directory that does not cryptographically validate against the `rootCA.pem` (either directly or via another valid intermediate).
   Write a Python script (or use OpenSSL commands) to validate all certificates in the directory against the root CA. Identify the filename of the single rogue certificate and write just its filename (e.g., `rogue.pem`) to `/home/user/rogue_cert.txt`.

4. **SSH Hardening & Remediation:**
   The attacker used the path traversal vulnerability to add a malicious SSH key to `/home/user/.ssh/authorized_keys`. Based on the log analysis (the timestamp of the attack), remove the attacker's SSH key from `/home/user/.ssh/authorized_keys` while leaving legitimate keys intact.
   Next, create a hardened SSH configuration snippet at `/home/user/hardened_sshd_config` that contains exactly the following directives to prevent future unauthorized access:
   - Disable password authentication.
   - Disable root login.
   - Allow only the user `user` to log in via SSH.

Ensure all output files are placed exactly as requested and follow the precise formats specified.