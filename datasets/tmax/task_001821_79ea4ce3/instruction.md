You are a security auditor tasked with fixing an insecure authentication validation tool.

We recently decommissioned a legacy service that handled user authentication, but we need to retain its exact token validation logic for processing archive logs. You have been provided with the original, highly flawed token parser in `/home/user/legacy_auth.cpp`.

During your initial service audit, you found that this legacy code is vulnerable to buffer overflows and improper input validation (CWE-120, CWE-190). Your job is to rewrite the authentication logic in C++ to be safe, while maintaining strict functional equivalence for *valid* legacy tokens.

Additionally, the original "Master PIN" used to salt the tokens was lost in the source code, but a previous admin left a snapshot of the server configuration dashboard. Examine the image located at `/app/admin_dashboard.png` to recover the 4-digit Master PIN.

Your new program must meet these requirements:
1. It must be written in C++ and compiled to `/home/user/check_auth`.
2. It should accept exactly one command-line argument: the authentication token string.
3. The token format is `USERID-TIMESTAMP-SIGNATURE`.
4. It must print `VALID` to standard output if the token is valid, and `INVALID` otherwise.
5. A token is valid if:
   - `USERID` is a positive integer.
   - `TIMESTAMP` is a positive integer.
   - `SIGNATURE` equals `(USERID * 3) + TIMESTAMP + MASTER_PIN`.
   - The token matches the exact format with hyphens.

Write the corrected C++ code, compile it to the specified path, and ensure it correctly validates tokens without crashing on malformed inputs.