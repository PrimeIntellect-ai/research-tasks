You are acting as a security auditor and deployment engineer for an older internal system. You have been tasked with auditing, fixing, and deploying a legacy Single Sign-On (SSO) authentication gateway.

The source code for this gateway is provided as a vendored Python package located at:
`/app/vendored/legacy-sso-server-1.0.0`

Your objective is to complete the following multi-stage workflow:

1. **Fix Package Perturbations**: 
   The vendored package is currently broken and cannot be run or installed properly. Inspect the source code (specifically `legacy_sso/auth.py` and `setup.py`) to find and fix the intentional syntax or import errors preventing it from functioning.

2. **Privilege Escalation Auditing & Patching**:
   The gateway has a known privilege escalation vulnerability. A developer left a backdoor that grants admin privileges based on a specific, easily spoofable HTTP header. 
   Find this backdoor in the request handling logic (within the vendored package) and remove it so that unauthorized users cannot bypass authentication.

3. **Password Cracking**:
   The gateway configuration file at `/app/vendored/legacy-sso-server-1.0.0/config.json` contains an MD5 hash for the `admin` user. 
   You must crack this hash using the wordlist provided at `/app/wordlist.txt`. 
   Once you have recovered the plaintext password, replace the hashed value in `config.json` with the plaintext password (under a new key `"admin_password_plaintext"`), as the updated gateway expects the plaintext password for its startup sequence.

4. **Deploy the Service**:
   Once the package is fixed and patched, run the gateway server. The server must be started so that it listens on `127.0.0.1` port `8080`.
   You can start the server by navigating to the vendored package directory and running:
   `python3 -m legacy_sso.server --port 8080 --config config.json`

Keep the server running in the background or foreground so that the automated verification system can interact with it.

The verification system will run programmatic tests against your running server to ensure:
- The server is up and listening on `127.0.0.1:8080`.
- The privilege escalation vulnerability has been successfully patched (sending the backdoor header will be rejected).
- The admin password was successfully cracked and configured, allowing legitimate login via the `/login` endpoint.
- Session payloads are correctly encoded and encrypted according to the server's internal logic.