You are a compliance analyst tasked with generating clean audit trails and evaluating a legacy C++ authentication service for security flaws.

You have been provided with a directory `/home/user/auth_system/` containing two files:
1. `auth_logger.cpp` - The source code for the authentication mechanism.
2. `old_logs.txt` - A file containing historical system logs.

Perform the following tasks to complete your audit:

1. **Authentication Flow Testing & Brute-Force:**
   Analyze the custom hashing algorithm in `auth_logger.cpp`. The system accepts a 4-digit PIN (0000 to 9999). Determine the single valid 4-digit PIN that successfully passes the authentication check. You may write a C++ or bash script to brute-force it. Save the valid 4-digit PIN to `/home/user/valid_pin.txt`.

2. **CWE Identification:**
   Review `auth_logger.cpp` to identify the security vulnerability present in its logging mechanism (logging a plaintext secret/credential). Identify the most specific Common Weakness Enumeration (CWE) identifier for "Insertion of Sensitive Information into Log File". Write the exact CWE identifier (format: `CWE-XXX`) to `/home/user/cwe_id.txt`.

3. **Sensitive Data Redaction:**
   Write a C++ program at `/home/user/redactor.cpp` that reads `/home/user/auth_system/old_logs.txt`. The program must identify any log entries formatted exactly as `[ERROR] Invalid attempt with PIN: <4-digit-pin>` and redact the PIN by replacing the digits with four asterisks (`****`). 
   - Non-matching lines or other numbers in the log must remain unmodified.
   - Compile your program and run it, writing the sanitized output to `/home/user/redacted_logs.txt`.

Ensure all files are saved in `/home/user/` with the exact names specified above.