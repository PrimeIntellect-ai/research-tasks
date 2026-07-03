You have been hired as a security auditor to evaluate a custom C-based authentication binary that is used to check permissions and grant access to the system's administration panel.

The source code for the authentication token validator is located at `/home/user/auth_checker.c`. 
This program takes a username and a token as arguments, computes the expected token based on internal logic, and compares it to the provided token to grant or deny access.

Your task is to:
1. Audit the code in `/home/user/auth_checker.c` to identify the primary security vulnerability that allows an attacker with source code access to generate valid tokens (identify the most specific, widely recognized CWE ID for hardcoded cryptographic secrets/salts).
2. Write a C program at `/home/user/generate_token.c` (or use shell/scripting utilities) to generate a valid authentication token for the username `admin`.
3. Create an audit report at `/home/user/audit_report.txt` containing exactly two lines in the following format:

```text
CWE: <CWE-ID>
Admin_Token: <64-character-hex-token>
```

Replace `<CWE-ID>` with the exact identifier (e.g., `CWE-123`) and `<64-character-hex-token>` with the valid SHA-256 hash token you generated for the `admin` user. Ensure all lowercase hex characters are used for the token.