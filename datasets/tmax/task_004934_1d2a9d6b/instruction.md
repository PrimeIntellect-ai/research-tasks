You are a security engineer tasked with securely rotating system credentials. During your audit, you discover that the legacy credential rotation script uses a flawed custom encryption mechanism and that previous executions have leaked sensitive data into a log file. 

Your objectives are to audit the script, crack an intercepted credential, redact the logs, and generate a final security report.

All files are located in `/home/user/cred_rotation/`.

**Objective 1: CWE Identification & Code Auditing**
Review the provided Python script `/home/user/cred_rotation/rotate.py`. Identify the specific CWE (Common Weakness Enumeration) identifier that corresponds to the vulnerability of "Use of a Broken or Risky Cryptographic Algorithm" present in this script's custom XOR encryption implementation.

**Objective 2: Cryptanalysis**
You have intercepted an encrypted master credential in `/home/user/cred_rotation/intercepted.txt` (represented as a hex string). You know that the legacy encryption uses a repeating 4-byte key and that all master credentials start with the exact string `MASTER_`. Perform a known-plaintext attack to recover the 4-byte key, and then decrypt the entire ciphertext to find the original master password.

**Objective 3: Sensitive Data Redaction**
The file `/home/user/cred_rotation/rotation.log` contains historical logs of password rotations. 
Unfortunately, it has leaked user email addresses and plaintext passwords. 
The log format is: `[YYYY-MM-DD] <email> rotated password to <password>`
You must parse this file and create a new file `/home/user/cred_rotation/rotation_redacted.log`. In the new file:
1. Replace all email addresses with exactly `[REDACTED_EMAIL]`
2. Replace the plaintext password at the end of the line with exactly `[REDACTED_CRED]`
Preserve the rest of the line format exactly.

**Objective 4: Security Report**
Create a file at `/home/user/cred_rotation/report.txt` containing exactly two lines:
Line 1: The CWE identifier from Objective 1 (Format: CWE-XXX)
Line 2: The decrypted master password from Objective 2

Ensure your final `report.txt` and `rotation_redacted.log` are formatted exactly as requested.