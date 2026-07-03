You are a forensics analyst investigating a compromised host. The attacker exploited a vulnerability in a web application's login flow to phish users, manipulated the server's TLS certificates, and dropped a suspicious Python payload.

Your task is to analyze the evidence, patch the vulnerability, identify the forged certificate, and safely analyze the payload using Python sandboxing techniques.

All evidence is located in `/home/user/evidence/`.

**Step 1: Code Auditing & CWE Identification**
Analyze the Flask web application code in `/home/user/evidence/server.py`. The attacker exploited an issue in the `/login` route where users are redirected after login. 
1. Identify the CWE ID for this specific vulnerability.
2. Patch `/home/user/evidence/server.py` so that the redirection is strictly limited to relative paths (it must start with a single `/` and not `//` or `http`). If an invalid path is provided, redirect to `/home`.
3. Append the CWE ID (e.g., "CWE-123") to `/home/user/report.txt` on the first line.

**Step 2: Certificate Chain Validation**
The attacker replaced the server's certificate. In `/home/user/evidence/certs/`, you will find `ca.crt` (the legitimate internal CA) and `server.crt` (the currently installed server certificate).
1. Programmatically verify `server.crt` against `ca.crt`. You will find that it fails verification because it was signed by a rogue CA.
2. Extract the Common Name (CN) of the *Issuer* of this rogue `server.crt`.
3. Append this Issuer CN exactly as it appears to the second line of `/home/user/report.txt`.

**Step 3: Process Isolation & Payload Analysis**
The attacker dropped `/home/user/evidence/payload.py`. You need to determine what file it attempts to steal without letting it actually read the file.
1. Write a Python script at `/home/user/sandbox.py`.
2. Your script must execute `payload.py` within the same process but use Python's `sys.addaudithook` to sandbox it.
3. The audit hook must intercept any attempt to `open` a file, block the action (by raising an exception or returning early before the file is opened), and capture the absolute file path the payload attempted to access.
4. Append the absolute file path targeted by the payload to the third line of `/home/user/report.txt`.

**Expected Output Format in `/home/user/report.txt`:**
```
CWE-XXX
Issuer Common Name
/path/to/targeted/file.ext
```