You are acting as a Compliance Analyst responsible for generating secure audit trails for a company's log processing pipeline. 

Your task involves identifying a tampered file, finding a security vulnerability within it, fixing the code, and securely packaging the results. All work must be done in the `/home/user/compliance` directory.

Here are your instructions:

1. **Integrity Verification:**
   You have been provided with a checksum file at `/home/user/compliance/checksums.sha256` containing the known-good SHA-256 hashes of the scripts located in `/home/user/compliance/scripts/`.
   Determine which script in the `scripts` directory has been tampered with (its hash will not match the checksum file).

2. **CWE Identification & Code Auditing:**
   Analyze the tampered script. An attacker modified it to introduce a critical security vulnerability that allows arbitrary OS command execution via improper neutralization of special elements. 
   Identify the official MITRE CWE ID for this specific vulnerability (e.g., CWE-79, CWE-89, etc.).
   Create a fixed version of the script that performs the same intended directory listing but safely handles user input without allowing command execution. Save this fixed bash script to `/home/user/compliance/fixed_script.sh`.

3. **Audit Trail Generation:**
   Create a text file at `/home/user/compliance/audit_report.txt` with exactly the following format (replace the bracketed placeholders with your findings):
   ```
   Tampered File: [filename of the tampered script, just the basename]
   Vulnerability: [The exact CWE ID, e.g., CWE-123]
   ```

4. **Encryption:**
   To protect the audit trail, encrypt `/home/user/compliance/audit_report.txt` using AES-256-CBC.
   Use PBKDF2 for key derivation.
   The passphrase is: `AuditSafe2024`
   Save the encrypted file to `/home/user/compliance/audit_report.enc`.

5. **Token Generation (HMAC):**
   Finally, generate an HMAC-SHA256 signature of the *encrypted* file (`audit_report.enc`) to ensure its integrity in transit. 
   Use the HMAC key: `integrity_key_99`
   Extract ONLY the hex string of the HMAC signature and save it to `/home/user/compliance/report.hmac`.