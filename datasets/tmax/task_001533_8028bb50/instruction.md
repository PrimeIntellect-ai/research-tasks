You are assisting a compliance analyst in auditing and securing an internal audit-logging utility. An existing C++ application is meant to safely log actions, but it has a security vulnerability and currently stores logs in plaintext. You must perform code auditing, fix the application, generate a log, encrypt it securely using a specific token, and enforce strict file permissions.

Follow these instructions carefully:

1. **Code Audit & Fix:** 
   Navigate to `/home/user/audit_app`. You will find a C++ source file named `logger.cpp`. 
   Analyze `logger.cpp` to identify the specific Common Weakness Enumeration (CWE) present in the logging logic (specifically related to how it formats user input).
   - Create a file `/home/user/audit_app/cwe_report.txt` and write ONLY the exact CWE ID (e.g., `CWE-123`) on the first line.
   - Edit `logger.cpp` to fix this vulnerability. Ensure it safely formats input strings without changing the file output location.

2. **Build & Run:**
   - Compile the fixed `logger.cpp` into an executable named `logger` in the same directory using standard C++ compiler (`g++`).
   - Run the executable, passing exactly this string as the first argument: `"USER_ACTION: Admin logged in"`
   - This will generate a plaintext log file named `raw_audit.log` in `/home/user/audit_app/`.

3. **Token Generation & Encryption:**
   We must encrypt the generated audit log using a key derived from a compliance token. 
   - Token: `COMPLIANCE_TOKEN_2024`
   - Calculate the SHA-256 hash of this exact token (no trailing newlines).
   - Use this hex-encoded SHA-256 hash as the 256-bit symmetric key to encrypt `raw_audit.log` using `openssl`.
   - Algorithm: AES-256-CBC
   - Initialization Vector (IV): A hardcoded 32-character hex string of all zeros (`00000000000000000000000000000000`).
   - Save the encrypted output to `/home/user/audit_app/secure_audit.enc`.

4. **Access Control & Cleanup:**
   - Modify the permissions of `/home/user/audit_app/secure_audit.enc` so that the file owner has read-only access, and the group and others have absolutely no permissions (octal 400).
   - Delete the plaintext `/home/user/audit_app/raw_audit.log` file so no unencrypted data remains.