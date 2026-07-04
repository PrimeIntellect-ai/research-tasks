You are a security engineer assigned to rotate the database credentials for a legacy C-based CGI authentication service. Before rotating the credentials, you must audit the application for security vulnerabilities, patch the C code, and secure the environment.

The application is located in `/home/user/legacy_auth_app`. 
The directory contains two files:
1. `app.c`: The source code of the CGI web application.
2. `creds.conf`: A configuration file containing the database password.

Perform the following tasks:

**Phase 1: Vulnerability Auditing**
Review `app.c` and `creds.conf`. You need to identify two major software weaknesses in the C code and a security misconfiguration regarding the credentials file.
Create a file at `/home/user/audit_report.txt` containing exactly three lines:
- Line 1: The formal CWE ID for the Cross-Site Scripting (XSS) vulnerability found in the code (Format: `CWE-XXX`).
- Line 2: The formal CWE ID for the Command Injection vulnerability found in the code (Format: `CWE-XXX`).
- Line 3: The initial octal file permissions of `creds.conf` before you make any changes (e.g., `0777`).

**Phase 2: Code Patching**
Modify `app.c` to fix the identified vulnerabilities. Implement strict input validation for the `username` parameter:
- The `username` must ONLY contain alphanumeric characters (A-Z, a-z, 0-9).
- If the `username` is missing, empty, or contains ANY non-alphanumeric characters, the program must print exactly `<html><body>Invalid input</body></html>` to `stdout` and exit with status code `1`.
- If the input is valid, the program should proceed with its normal execution (logging and printing the success/failure message).

Compile your patched code using:
`gcc /home/user/legacy_auth_app/app.c -o /home/user/legacy_auth_app/auth_app.cgi`

**Phase 3: Credential Rotation & Access Control**
1. Open `/home/user/legacy_auth_app/creds.conf` and replace the old password with the new rotated credential: `SuperSecretRotate99!` (preserve the `DB_PASS=` key format).
2. The current file permissions on `creds.conf` are insecure. Restrict the file permissions of `creds.conf` so that only the owner has read and write access, and no one else has any access.

Complete these steps using only the terminal. You may test your compiled CGI application by setting the `QUERY_STRING` environment variable before executing `./auth_app.cgi`.