You are a DevSecOps engineer tasked with enforcing security policies as code for a legacy application. You need to write and execute a Bash script that audits and remediates several security misconfigurations on the local system.

You have been provided with the following files in `/home/user/`:
1. `/home/user/legacy.conf`: A configuration file containing a weak hashed database password.
2. `/home/user/wordlist.txt`: A dictionary of common weak passwords.
3. `/home/user/app.log`: An application log file that accidentally leaked sensitive AWS credentials.
4. `/home/user/certs/legacy.crt`: The current SSL certificate used by the legacy service.

Your objective is to perform the following actions and generate a summary report:

1. **Password Cracking / Auditing:**
   Extract the MD5 hash assigned to `db_password_hash` in `/home/user/legacy.conf`. Use the provided `/home/user/wordlist.txt` to crack this hash (you can write a short Bash loop using `md5sum` or use standard tools if available). Note the cracked plaintext password.

2. **Sensitive Data Redaction:**
   Scan `/home/user/app.log` for exposed AWS Access Key IDs. An AWS Access Key ID in this log always starts with `AKIA` followed by exactly 16 uppercase alphanumeric characters (A-Z, 0-9). 
   Create a new file at `/home/user/app_redacted.log` where every matched AWS key is replaced with `AKIA[REDACTED]`. (For example, `AKIAIOSFODNN7EXAMPLE` becomes `AKIA[REDACTED]`).

3. **TLS/SSL Certificate Management:**
   Check the expiration date of the certificate at `/home/user/certs/legacy.crt`. If the certificate is already expired, or expires within 7 days of the current date, you must generate a new self-signed certificate to replace it.
   If replacement is needed, use `openssl` to generate a new RSA 2048-bit private key (`/home/user/certs/new.key`) and a self-signed certificate (`/home/user/certs/new.crt`) valid for 365 days. The Common Name (CN) for the new certificate MUST be exactly `secure.local`.

4. **Reporting:**
   Create a final audit report at `/home/user/audit_report.txt` with exactly the following three lines (replace the bracketed placeholders with your findings):
   ```
   CRACKED_PASSWORD: <plaintext_password>
   REDACTED_COUNT: <number_of_keys_redacted>
   CERT_ACTION: <"REPLACED" if a new cert was generated, or "VALID" if not>
   ```

You may use any standard Linux utilities available in the terminal.