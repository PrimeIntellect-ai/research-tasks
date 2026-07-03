You are a penetration tester auditing a local service and setting up a hardened proof-of-concept. You have gained access to a directory `/home/user/audit` containing several files, but you need to retrieve a secret token and harden an insecure web service.

Your objectives are:

1. **Password Cracking**: 
   In `/home/user/audit/target.hash`, there is a SHA-256 hash of a service password.
   In `/home/user/audit/wordlist.txt`, there is a list of potential passwords.
   Determine the original password by brute-forcing or hashing the words in the wordlist.

2. **Token Generation**:
   Once you have the password, use the provided script `/home/user/audit/auth_gen.py` to generate an authentication token. You must run it like so: `python3 /home/user/audit/auth_gen.py <CRACKED_PASSWORD>`.

3. **Content Security Policy (CSP) Enforcement**:
   The file `/home/user/audit/server.py` contains a basic Python HTTP server that is missing security headers. Modify `server.py` so that every HTTP 200 response it serves includes the exact following header:
   `Content-Security-Policy: default-src 'self'; script-src 'none';`

4. **Process Isolation / Sandboxing Wrapper**:
   You must create a Bash script at `/home/user/sandbox.sh` that runs the modified `server.py` in a constrained environment. The script must:
   - Use `env -i` to clear all environment variables.
   - Explicitly set `PATH=/usr/bin:/usr/local/bin:/bin`
   - Explicitly pass the token you generated as an environment variable named `AUTH_TOKEN`.
   - Start the python server (e.g., `python3 /home/user/audit/server.py`).
   Ensure the script is executable (`chmod +x /home/user/sandbox.sh`).

5. **Reporting**:
   Create a file `/home/user/result.log` with exactly two lines:
   - Line 1: The cracked password.
   - Line 2: The generated token.

Do not start the server yourself as a background process; our automated testing suite will execute `/home/user/sandbox.sh` and make HTTP requests to verify the CSP headers and the `AUTH_TOKEN` environment variable.