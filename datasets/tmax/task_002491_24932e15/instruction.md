You are acting as a penetration tester and security engineer. We have intercepted an administrator's note containing a master key, and captured a proprietary authentication module used by the target. 

Your objectives are to extract the key, reverse-engineer the authentication module, and set up a secure proxy service that correctly validates requests based on the extracted key. Additionally, you must produce a hardened SSH configuration file.

Step 1: Information Extraction (Image Analysis)
There is an image file located at `/app/admin_note.png`. It contains a handwritten or printed master key. Use OCR tools (like `tesseract`, which is preinstalled) to extract the text. Identify the 8-character hex string following "MASTER_KEY=".

Step 2: Reverse Engineering
You are provided with an obfuscated Python script at `/app/auth_module.py`. This script contains a function `generate_token(master_key: str, challenge: int) -> str`. Analyze or reverse-engineer this script to understand how it calculates the token. 

Step 3: Secure Proxy Service (Multi-Protocol Verification)
Write and run a Python HTTP server listening on `127.0.0.1:8080`. 
The server must expose an endpoint: `GET /scan`
Clients will send requests with two headers:
- `X-Challenge`: An integer value (e.g., 42)
- `X-Auth-Token`: The generated token for that challenge using the extracted `MASTER_KEY`.

Your server must:
1. Read the `X-Challenge` header.
2. Use the reverse-engineered logic and the extracted `MASTER_KEY` to compute the expected token.
3. Compare the expected token with the `X-Auth-Token` header.
4. If they match, return an HTTP 200 OK with the exact text: `SCAN_AUTHORIZED`.
5. If they do not match, return an HTTP 403 Forbidden with the exact text: `ACCESS_DENIED`.

Step 4: SSH Hardening Configuration
To secure our own infrastructure, generate a hardened SSH configuration file at `/home/user/sshd_config_hardened`. The file must contain exactly the following directives (and no others, ignoring comments):
- `PermitRootLogin no`
- `PasswordAuthentication no`
- `X11Forwarding no`
- `MaxAuthTries 3`
- `Protocol 2`

Keep the HTTP server running in the background or foreground so it can be verified by our automated test suite.