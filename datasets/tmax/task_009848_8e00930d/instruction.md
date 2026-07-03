You are a security engineer tasked with rotating credentials and auditing a compromised internal web service. The service files are located in `/home/user/service`. 

Perform the following security tasks using Bash commands and standard Linux utilities:

1. **Privilege Escalation Audit**: 
   An attacker might have left a backdoor by setting the SUID bit on binaries. Scan the directory `/home/user/service/bin` for any files with the SUID bit set. 
   - Write the absolute paths of any discovered SUID files to `/home/user/audit_suid.txt` (one path per line).
   - Remove the SUID bit from these files so they are no longer a risk.

2. **File Integrity Verification**:
   The directory `/home/user/service/public` contains the web assets. A cryptographic hash file is provided at `/home/user/service/hashes.txt` (in standard `sha256sum` format).
   - Verify the files against the hashes. 
   - Exactly one file has been modified by the attacker. Identify this file and write its absolute path to `/home/user/compromised_file.txt`.

3. **HTTP Header Inspection**:
   We intercepted a suspicious HTTP response from the server, saved at `/home/user/service/logs/response.bin`.
   - Parse this raw HTTP response to find the `Set-Cookie` header associated with the cookie named `admin_session`.
   - Extract *only* the value of the `admin_session` cookie (excluding the cookie name, path, or other attributes).
   - Write this extracted value to `/home/user/stolen_cookie.txt`.

4. **Credential Rotation**:
   The current TLS certificate and private key at `/home/user/service/cert/server.crt` and `/home/user/service/cert/server.key` are compromised.
   - Generate a new 2048-bit RSA private key and a new self-signed X.509 certificate.
   - The certificate must be valid for exactly 30 days and have the Common Name (CN) set to `localhost`.
   - Overwrite the existing `/home/user/service/cert/server.key` and `/home/user/service/cert/server.crt` with your newly generated files.

Ensure all output files are placed exactly as requested, with no extra whitespace or text unless specified.