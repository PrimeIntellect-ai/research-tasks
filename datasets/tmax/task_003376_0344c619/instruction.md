You are acting as an automated security auditor and remediation agent. A previous administrator left behind an incomplete server configuration. You need to analyze the security policy, enforce access controls, verify cryptographic hashes, establish a basic TLS configuration, and scan for simple vulnerabilities.

Your instructions are as follows:

1. **Policy Extraction:** 
   There is an image containing the security policy located at `/app/policy.png`. Extract the text from this image (you may use `tesseract` or any other tool). The image contains specific required file permissions and a target SHA-256 hash for a critical binary.

2. **Access Control Enforcement:**
   Apply the exact octal file permissions stated in the policy image to the corresponding files in `/home/user/app/`. 

3. **Cryptographic Integrity:**
   The current executable at `/home/user/app/bin/secure_exec` is corrupted. The policy image states the correct expected SHA-256 hash. You will find several backup binaries in `/home/user/backups/`. Identify which backup matches the expected hash, and replace `/home/user/app/bin/secure_exec` with the valid backup.

4. **TLS Management:**
   Generate a self-signed TLS certificate for the internal service. 
   - Output files must be `/home/user/app/certs/server.crt` and `/home/user/app/certs/server.key`.
   - The certificate must have the Common Name (CN) exactly set to `secure-internal.local`.
   - Ensure you apply the `server.key` permissions required by the policy image.

5. **Vulnerability Scanning:**
   Scan the directory `/home/user/app/source/` for hardcoded secrets. Specifically, look for any files containing lines that match the regex pattern: `(?i)password\s*=\s*['"][^'"]+['"]`
   Save your findings in a JSON file at `/home/user/vuln_report.json`. The file should contain a single JSON array of strings, where each string is the absolute path to a file containing at least one hardcoded secret.

You may use Python, Bash, or any other tools available to complete these tasks. Do not delete the backup binaries. Ensure all final paths match the specifications exactly.