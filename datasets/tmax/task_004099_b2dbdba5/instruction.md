You have been assigned to perform a security audit on a legacy authentication system. Your task involves analyzing logs, reverse engineering an old authentication module, inspecting a TLS certificate, and demonstrating a JWT vulnerability.

Here is what you need to do:

1. **Log Parsing and JWT Forgery**:
   You are provided with a security log file at `/home/user/auth.log`. This log contains various authentication events, including successful logins that log a JWT token.
   - Parse `/home/user/auth.log` to find the valid JWT token assigned to the user `guest_user`.
   - The system is vulnerable to the `alg="none"` attack. Craft a forged JWT token for `guest_user` but elevate their privileges by changing their `"role"` to `"admin"`. Keep all other fields in the payload the same as the original token.
   - Write the forged token (Header.Payload.Signature) to `/home/user/forged_token.txt`. Note: Ensure you use Base64Url encoding without padding, and the signature part should be empty.

2. **TLS Certificate Analysis**:
   Inspect the server's TLS certificate located at `/home/user/server.crt`.
   - Extract the Expiration Date (Not After) in `YYYY-MM-DD` format.
   - Extract the Subject Alternative Names (SANs) as a comma-separated list of DNS names (e.g., `example.com, www.example.com`).
   - Create a report at `/home/user/cert_report.txt` with exactly the following format:
     ```
     Expiration: YYYY-MM-DD
     SANs: <dns_name_1>, <dns_name_2>
     ```

3. **Reverse Engineering**:
   There is a compiled Python 3.10 bytecode file at `/home/user/legacy_auth.pyc`.
   - Disassemble or reverse engineer this file to locate a hardcoded API key stored in the `API_KEY` variable.
   - Save only the exact value of the API key to `/home/user/api_key.txt`.

You will need to use your shell and Python skills to accomplish this. Ensure all output files are exactly as specified.