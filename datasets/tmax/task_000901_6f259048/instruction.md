You are a security engineer tasked with rotating credentials and fixing a vulnerability in a legacy authentication service.

You have been given access to the following files:
1. `/home/user/auth_service.cpp`: The source code for a simple authentication binary. It currently has a critical vulnerability related to how it stores and validates tokens.
2. `/home/user/service.log`: A log file that has historically leaked the old authentication token.

Perform the following tasks:

1. **Code Audit & Fix**: Inspect `/home/user/auth_service.cpp`. Identify the vulnerability where the credential is inappropriately stored in the code. Modify the C++ code to eliminate this vulnerability. The program must now read the valid expected token from the first line of a file located at `/home/user/auth.token` and compare it against the token provided as the first command-line argument (`argv[1]`). The output format ("Access Granted" or "Access Denied") must remain exactly the same.
2. **Token Generation**: Generate a new, random cryptographic token consisting of exactly 32 lowercase hexadecimal characters. Save this token to `/home/user/auth.token`.
3. **Compilation**: Compile your updated C++ program and save the executable to `/home/user/auth_service`. Use `g++`.
4. **Data Redaction**: Identify the leaked old token in `/home/user/service.log`. Replace every instance of the old token in this file with the exact string `[REDACTED]`. Do not change any other content in the log file.
5. **Reporting**: Create a file at `/home/user/report.txt` containing exactly two lines:
   - Line 1: The standard MITRE CWE identifier for the vulnerability you fixed in the C++ code (format: `CWE-XXX`, for example `CWE-798` or `CWE-200`).
   - Line 2: The exact newly generated 32-character hex token.

Ensure the final executable correctly grants access when provided with the new token.