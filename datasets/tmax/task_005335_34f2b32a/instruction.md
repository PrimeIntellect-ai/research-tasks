You are a forensics analyst investigating a compromised Linux host. The attacker left behind an encrypted staging file, a dropped RSA private key, and traces in the web server access logs. Your objective is to recover the stolen data, decrypt it, redact any Personally Identifiable Information (PII), and save the sanitized evidence.

You have been provided a directory `/home/user/evidence/` containing:
- `access.log`: The web server access logs.
- `attacker.key`: The attacker's RSA private key (PEM format).
- `staging.enc`: The encrypted payload left by the attacker.

Perform the following steps using Python (you may install necessary libraries like `cryptography` using pip):

1. **Log Parsing & Cookie Inspection:**
   Analyze `/home/user/evidence/access.log`. Locate the HTTP POST request made to the `/api/exfiltrate` endpoint that resulted in a `201` (Created) status code. Extract the value of the `Session-Token` cookie from this log entry.

2. **RSA Decryption:**
   The `Session-Token` cookie value is Base64 encoded. Decode it, then decrypt it using the RSA private key (`/home/user/evidence/attacker.key`). The encryption used PKCS#1 v1.5 padding. The decrypted value is a raw 32-byte AES key.

3. **AES Decryption:**
   Read `/home/user/evidence/staging.enc`. The first 16 bytes of this file represent the Initialization Vector (IV). The remainder of the file is the ciphertext. Decrypt the ciphertext using AES-256-CBC with the extracted IV and the 32-byte AES key you recovered in Step 2. Decode the decrypted payload as UTF-8 plaintext.

4. **Sensitive Data Redaction:**
   The decrypted plaintext contains stolen PII. You must redact this information to sanitize the evidence:
   - Replace all IPv4 addresses with the exact string `[REDACTED_IP]`
   - Replace all email addresses with the exact string `[REDACTED_EMAIL]`
   *(Assume standard formats for IPv4 and email addresses).*

5. **Output Generation:**
   Save the final, redacted plaintext to `/home/user/evidence/recovered_clean.txt`. Ensure no extra newlines or trailing spaces are added beyond what is in the redacted plaintext.

Write and execute a Python script to automate this recovery process.