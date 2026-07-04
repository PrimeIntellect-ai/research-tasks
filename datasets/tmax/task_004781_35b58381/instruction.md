You are a security engineer tasked with rotating a compromised database credential and fixing a vulnerability in a legacy Go application.

The application source code is located at `/home/user/app.go`. Currently, this application accepts the database password via a command-line flag (`--password`). This is a severe security risk because command-line arguments are visible system-wide to all users via `/proc/[pid]/cmdline`.

Your task requires you to perform the following steps:

1. **Code Auditing & Remediation**: 
   Modify `/home/user/app.go` to completely remove the `--password` command-line flag. Instead, the application must read the password exclusively from an environment variable named `DB_PASSWORD`. Ensure the application logic otherwise remains the same (it should still process the `username` flag and connect).
   Compile your updated code and save the binary as `/home/user/app_secure`.

2. **Payload Decoding & Rotation**:
   The new database credential has been provisioned and securely delivered in a Base64-encoded file at `/home/user/vault.b64`. Decode this payload to retrieve the new plaintext password. 

3. **Intrusion Detection Pattern Matching**:
   To prevent this from happening in other legacy scripts, create a PCRE regular expression that matches any command-line invocation containing the string `--password=` followed by one or more non-whitespace characters. 
   Save ONLY the raw regular expression (no explanations or extra text) in `/home/user/id_rule.txt`.

4. **Reporting**:
   Create a report file at `/home/user/rotation_summary.txt` with exactly two lines:
   - Line 1: The exact CWE (Common Weakness Enumeration) ID that best describes the vulnerability of exposing credentials via command-line arguments or process environment (e.g., CWE-XXX).
   - Line 2: The decoded plaintext password.

Ensure all requested files are placed exactly at the specified absolute paths.