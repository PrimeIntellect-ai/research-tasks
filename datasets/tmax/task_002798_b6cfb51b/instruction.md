You are acting as a security auditor reviewing a system's backup and logging infrastructure. You need to identify permission issues, perform a basic cryptographic extraction, identify security weaknesses (CWEs), and redact sensitive data. Use only standard bash tools and coreutils.

Perform the following tasks:

1. **Permission Auditing**: 
   Find all files in `/home/user/audit_target` that are world-writable (permissions `o+w`). Write the absolute paths of these files to `/home/user/vulnerable_perms.txt` (one path per line).

2. **CWE Identification**:
   Review the script `/home/user/audit_target/encrypt.sh`. It contains a flawed, custom encryption routine that hardcodes a shift value (Caesar cipher) instead of using a strong algorithm. Identify the MITRE CWE IDs for:
   - "Use of a Broken or Risky Cryptographic Algorithm"
   - "Use of Hard-coded Credentials" (since the secret shift key is hardcoded)
   Write these two CWE IDs (format: `CWE-XXX`) to `/home/user/cwe_report.txt`, one per line, in ascending numerical order.

3. **Algorithmic Cryptanalysis**:
   The file `/home/user/audit_target/secret_data.enc` was encrypted using the script mentioned above. You know via a known-plaintext assumption that the original text begins exactly with the string `CONFIDENTIAL: `. 
   Determine the shift used by analyzing the ciphertext, decrypt the entire contents of `secret_data.enc`, and write the plaintext to `/home/user/decrypted_data.txt`.

4. **Data Redaction**:
   The file `/home/user/audit_target/server.log` contains sensitive information that must be redacted.
   - Find all 16-digit credit card numbers (contiguous sequences of exactly 16 digits) and replace them with `XXXX-XXXX-XXXX-XXXX`.
   - Find all API keys in the format `API_KEY=<16 alphanumeric characters>` and replace the alphanumeric characters with `REDACTED` (e.g., `API_KEY=REDACTED`).
   Write the sanitized output to `/home/user/redacted_server.log`.