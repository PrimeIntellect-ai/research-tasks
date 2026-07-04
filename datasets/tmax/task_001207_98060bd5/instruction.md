You are acting as a penetration tester tasked with analyzing an evidence bundle from a compromised web server. 

You have been provided with an evidence bundle located at `/home/user/audit/`. Your objective is to perform a comprehensive security analysis and algorithmic data processing task, combining file integrity verification, vulnerability analysis, password cracking, and data redaction. 

Please perform the following steps:

1. **File Integrity Verification**: 
   The directory `/home/user/audit/` contains a `manifest.sha256` file with the expected SHA-256 hashes of the files in the directory. One file in the directory has been tampered with and does not match its hash in the manifest. Identify the name of this tampered file.

2. **Password Cracking**:
   The file `/home/user/audit/users.db` is an SQLite database containing a `users` table with columns `username` and `password_hash`. The hashes are MD5. Use the provided wordlist at `/home/user/audit/wordlist.txt` to crack all the password hashes.

3. **Vulnerability Analysis**:
   The file `/home/user/audit/server.py` is the source code for the compromised web application. Analyze the file to find two critical vulnerabilities:
   - A SQL Injection (SQLi) vulnerability. Identify the exact line number where the vulnerable database query is executed.
   - A Cross-Site Scripting (XSS) vulnerability. Identify the exact line number where unescaped user input is directly returned in an HTML response.

4. **Sensitive Data Redaction**:
   The file `/home/user/audit/messages.txt` contains user communications that leaked sensitive credit card numbers. You must redact these credit card numbers. 
   - A credit card number is defined as exactly 16 digits separated by hyphens in the format: `DDDD-DDDD-DDDD-DDDD` (where D is a digit).
   - Replace the first 12 digits with `X`, leaving only the last 4 digits intact. (e.g., `1234-5678-9012-3456` becomes `XXXX-XXXX-XXXX-3456`).
   - Save the fully redacted file to `/home/user/audit/messages_redacted.txt`.
   - Calculate the SHA-256 hash of the resulting `/home/user/audit/messages_redacted.txt` file.

**Deliverable**:
Generate a JSON report of your findings and save it to `/home/user/report.json`. The JSON file must strictly follow this exact structure:

```json
{
  "tampered_file": "filename.ext",
  "cracked_passwords": {
    "user1": "plaintext1",
    "user2": "plaintext2"
  },
  "vulnerabilities": {
    "sqli_line": 10,
    "xss_line": 20
  },
  "redacted_hash": "sha256_hash_of_messages_redacted.txt_here"
}
```

Ensure all line numbers are integers and hashes are lowercase hex strings.