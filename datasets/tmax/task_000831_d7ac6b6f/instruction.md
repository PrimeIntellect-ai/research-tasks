You are a security engineer tasked with securing a legacy authentication service located in `/home/user/service`. The service consists of a web server (`server.py`), an authentication wrapper script (`wrapper.py`), and a compiled backend binary (`auth_bin`).

Your security audit has revealed several critical vulnerabilities that you must fix:

1. **Credential Leakage via `/proc`**:
   The `wrapper.py` script currently hardcodes the authentication token and passes it to the `auth_bin` executable as a command-line argument. This leaks the token to any local user via `/proc`. 
   * Reverse engineer or analyze the `/home/user/service/auth_bin` executable to discover the specific environment variable it accepts for secure token injection.
   * Rewrite `/home/user/service/wrapper.py` to read the token from `/home/user/service/token.txt` and pass it to `auth_bin` exclusively via this newly discovered environment variable. Ensure the token is *no longer* passed as a command-line argument.

2. **Credential Rotation**:
   The current token is compromised. 
   * Generate a new secure 32-character lowercase hexadecimal token.
   * Save this new token to `/home/user/service/token.txt`. (The `auth_bin` uses this file as its source of truth to validate incoming authentication attempts).

3. **Network Policy Configuration**:
   The web server in `/home/user/service/server.py` currently binds to all interfaces (`0.0.0.0`), exposing it externally. 
   * Modify `server.py` so that it exclusively binds to the local loopback address (`127.0.0.1`).

4. **Content Security Policy (CSP) Enforcement**:
   The web server does not send any CSP headers, leaving it vulnerable to XSS.
   * Modify `/home/user/service/server.py` to include the HTTP response header: `Content-Security-Policy: default-src 'self';`

Finally, to document your fixes, create a JSON report at `/home/user/security_report.json` with the following structure:
```json
{
  "new_token": "<your_32_char_hex_token>",
  "env_var_discovered": "<the_environment_variable_name_auth_bin_checks>"
}
```

Constraints:
- Do not modify `auth_bin`. You only have the compiled executable.
- Do not change the file paths or names of the existing scripts.
- Ensure the authentication flow still works (i.e., `wrapper.py` exits with code 0 when run).