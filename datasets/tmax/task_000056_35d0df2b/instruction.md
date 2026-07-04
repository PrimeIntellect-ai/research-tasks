You are a compliance analyst tasked with generating secure audit trails from raw web server access logs. The raw logs contain sensitive customer information and evidence of potential cyberattacks. 

Your objective is to write a C++ program that processes these logs to detect intrusions, redact sensitive data, and encrypt the final audit log to meet compliance requirements.

Working Directory: `/home/user/audit_task/`

Input Files provided in the working directory:
1. `raw_access.log`: The raw web server access log.
2. `key.bin`: A 32-byte binary file containing the AES-256 encryption key.
3. `iv.bin`: A 16-byte binary file containing the AES-256 initialization vector (IV).

You must write a C++ program named `/home/user/audit_task/audit_processor.cpp`. The program must compile successfully with `g++ -std=c++17 audit_processor.cpp -o audit_processor -lssl -lcrypto`.

The compiled program must accept exactly three command-line arguments in this order:
`./audit_processor <input_log_path> <output_encrypted_log_path> <report_file_path>`

The program must perform the following tasks:
1. **Intrusion Detection**: Analyze each line of the log file for common attack patterns. A line is considered an intrusion attempt if it contains either of the following exact substrings:
   - `../` (Path Traversal)
   - `' OR '1'='1` (SQL Injection)

2. **Sensitive Data Redaction**: Before writing any line to the final log, you must redact sensitive information:
   - Credit Cards: Find any instance of `cc=` followed by exactly 16 digits. Replace the 16 digits with `[REDACTED]`. For example, `cc=1234567812345678` becomes `cc=[REDACTED]`.
   - Session Tokens: Find any instance of `token=` followed by one or more alphanumeric characters until a space or non-alphanumeric character (e.g., `token=abc123xyz&` or `token=abc123xyz HTTP`). Replace the token value with `[REDACTED]`. For example, `token=abc123xyz` becomes `token=[REDACTED]`.

3. **Encryption**: The redacted log data must be encrypted in memory using the AES-256-CBC algorithm (using OpenSSL's EVP API) with the key from `key.bin` and IV from `iv.bin`. The encrypted binary ciphertext must be written directly to `<output_encrypted_log_path>`. (Do not write the plaintext redacted log to disk).

4. **Reporting**: The program must write a summary report to `<report_file_path>` in plaintext with exactly the following format:
   ```
   Total lines: <number>
   Redacted lines: <number>
   Intrusions detected: <number>
   ```
   *(Note: "Redacted lines" counts the number of lines where at least one redaction occurred).*

When you are finished, build your program and run it using the files in `/home/user/audit_task/` to produce `/home/user/audit_task/secure_audit.enc` and `/home/user/audit_task/audit_report.txt`.