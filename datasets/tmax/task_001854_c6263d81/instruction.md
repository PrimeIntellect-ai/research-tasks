You are an incident responder investigating a security breach on a custom web authentication server. You have identified several issues in the login flow, including exposed credentials in logs, a potential privilege escalation vector via command injection in the CGI binary, an open redirect vulnerability, and missing security headers.

Your objective is to remediate these issues by performing the following tasks:

1. **Sensitive Data Redaction**:
   The file `/home/user/auth_requests.log` contains raw HTTP request logs. Many lines contain a query string with sensitive passwords (e.g., `&pwd=Secret123&` or `?pwd=Secret123 `). 
   Use standard bash text processing tools to read this file and replace the actual password values with the exact string `[REDACTED]`. Keep the rest of the line intact (e.g., `&pwd=[REDACTED]&`). Save the cleaned output to `/home/user/redacted_requests.log`.

2. **Privilege Escalation & Vulnerability Remediation**:
   The custom server CGI source code is located at `/home/user/auth_cgi.c`. Audit and modify this C code to fix the following issues:
   - **Command Injection (Privilege Escalation risk)**: The `log_access` function uses `system()` to echo logs, which allows command injection if a malicious username is provided. Replace the `system()` call with safe standard C file I/O functions (`fopen`, `fprintf`, `fclose`) to append the log message "Access by <user>\n" directly to `/home/user/access.log`.
   - **Open Redirect**: The login flow takes a `redirect` parameter and directly outputs it in a `Location:` HTTP header. Modify the code so that the `Location:` header is ONLY printed if the `redirect` string strictly begins with a single forward slash `/` and does NOT begin with `//` (to prevent protocol-relative URL bypasses), `http://`, or `https://`.
   - **Content Security Policy**: Enforce a strict CSP by adding the HTTP header `Content-Security-Policy: default-src 'self';` to the server's output, immediately before the blank line that separates headers from the body.

3. **Compilation**:
   Compile your patched C code using `gcc` and output the binary to `/home/user/auth_cgi`. Do not add any special compiler flags, just compile it successfully.

Ensure all file paths are exactly as specified. Do not remove the original `/home/user/auth_cgi.c` or `/home/user/auth_requests.log` files.