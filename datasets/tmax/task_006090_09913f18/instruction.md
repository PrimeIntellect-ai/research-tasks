You are acting as a compliance analyst generating an audit trail for a legacy login application that is suspected of containing an open redirect vulnerability.

You are provided with a compiled ELF binary at `/home/user/login_handler` and a directory of certificates at `/home/user/certs/` (containing `ca.crt`, `intermediate.crt`, and `server.crt`).

Your task is to generate three audit logs using Bash commands:

1. **File Permissions Audit:** 
   Check the exact file permissions of the `/home/user/login_handler` binary. Write the 10-character permission string (e.g., `-rwxr-xr-x`) to `/home/user/permissions.log`.

2. **Binary Vulnerability Analysis:**
   The `login_handler` binary contains a hardcoded open redirect URL used in its flawed login flow. The URL begins with `https://malicious.example.com`. Extract the full malicious URL from the binary and write it to `/home/user/vulnerability.log`.

3. **Certificate Chain Validation:**
   Verify the certificate chain for the login server. You must check if `server.crt` is properly signed and valid according to the provided `intermediate.crt` and root `ca.crt`. 
   If the certificate chain is valid, write the word `VALID` to `/home/user/cert_status.log`. If it is invalid, write `INVALID`.

Ensure all log files are placed exactly in `/home/user/` and contain only the requested data without any extra characters or newlines (a single trailing newline is acceptable).