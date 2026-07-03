You are a DevSecOps engineer tasked with enforcing "policy as code" and auditing a legacy C-based authentication daemon. The daemon's source code is located at `/home/user/auth_daemon`. 

Currently, the daemon has several critical security issues: it has a buffer overflow vulnerability in its HTTP header parsing logic, it fails to properly implement our custom cryptographic token verification policy, and it leaves sensitive key files overly permissive.

Your task is to fix these issues, deploy the daemon, and generate an audit log.

**Requirements:**

1. **Code Audit & Fixes (CWE Identification & Secure Coding):**
   - Inspect `/home/user/auth_daemon/daemon.c`.
   - Identify and fix the classic buffer overflow vulnerability in the `parse_cookie()` function, which unsafely extracts the `auth_token` value from the `Cookie: ` header into a small fixed-size buffer. 
   - Ensure the extracted token string is safely bounded and null-terminated.

2. **Cryptographic Authentication Policy Enforcement:**
   - In `daemon.c`, there is a function `validate_token(const char *hex_token)`. It is currently hardcoded to return `1` (true).
   - Update `validate_token` to implement the correct policy: The system has a 16-byte secret key stored in `/home/user/auth_daemon/secret.key`. The expected valid `hex_token` is the hex-encoded representation (lowercase, 32 characters) of the bytes in `secret.key` XORed with the constant byte `0x7F`.
   - The daemon should return an HTTP 200 response if the token matches, and HTTP 403 if it does not.

3. **Access Control Configuration:**
   - The file `/home/user/auth_daemon/secret.key` currently has dangerous permissions (`0777`).
   - Modify its permissions so that it is strictly read-only for the owner, with no access for group or others.

4. **Build and Deploy:**
   - Recompile the daemon using the provided `Makefile` in `/home/user/auth_daemon`.
   - Start the daemon in the background. It will bind to `127.0.0.1:9000`.

5. **Verification & Logging:**
   - Write a bash script `/home/user/test_auth.sh` that:
     - Calculates the correct expected hex token based on the policy.
     - Sends an HTTP GET request to `http://127.0.0.1:9000/` with the header `Cookie: auth_token=<valid_hex_token>`.
     - Sends a second request with an invalid token `Cookie: auth_token=badtoken`.
     - Sends a third request with a massive token (200 'A's) to ensure the daemon does not crash.
   - Output the results of your actions to a log file at `/home/user/audit_report.log` with the following strict format:
     ```
     PERMISSIONS: [The octal permissions of secret.key, e.g., 400]
     CWE_FIXED: [The CWE ID of the buffer overflow you fixed, e.g., CWE-120]
     VALID_RESPONSE: [The HTTP status code from the valid token request]
     INVALID_RESPONSE: [The HTTP status code from the invalid token request]
     CRASH_TEST: [SUCCESS if the daemon is still running after the large payload, FAILED otherwise]
     ```