You are a penetration tester performing a security assessment on a pre-release version of a custom Python web application and its accompanying local reverse-proxy configuration. The application files are located in `/home/user/app`.

There are several security weaknesses in the application's implementation. Your goal is to identify these weaknesses, exploit the cryptographic flaw to escalate privileges, patch the application's headers, and update the network configuration.

Here are the details of the environment:
1.  **Vulnerable Application:** The main application code is at `/home/user/app/app.py`. It uses a custom token generation scheme for user authentication cookies and currently has no protection against Cross-Site Scripting (XSS).
2.  **Network Policy:** A JSON file at `/home/user/app/network_policy.json` acts as an application-level firewall configuration. Currently, it drops all traffic to the `/admin` endpoint.

Your tasks are to perform the following actions:

**1. Vulnerability Identification (CWE):**
Audit the `/home/user/app/app.py` source code. Identify the Common Weakness Enumeration (CWE) IDs for:
a) The broken/risky cryptographic algorithm used for the session tokens.
b) The missing defense-in-depth mechanism (specifically, the lack of Content Security Policy / protection mechanism failure).
Create a file at `/home/user/cwe_report.txt` containing exactly two lines, each with the format `CWE-XXX` (where XXX is the appropriate number).

**2. Cryptanalysis & Privilege Escalation:**
The application issues authentication tokens by XORing the user's role string with a repeating 4-byte secret key and hex-encoding the result. 
You registered a guest account and intercepted your token. 
Your guest plaintext is: `role=guest`
Your intercepted hex token is: `015c0f374e5416370047`

Using cryptanalysis, write a Python script at `/home/user/forge.py` that recovers the 4-byte secret key from the guest token and generates a new, valid hex token for the plaintext `role=admin`.
Run your script and save the resulting admin token string (just the hex string, no newlines or other text) to `/home/user/admin_token.txt`.

**3. Content Security Policy Enforcement:**
Modify the Flask application in `/home/user/app/app.py`. Update the `after_request` hook (or add one) so that *every* HTTP response includes the following header exactly:
`Content-Security-Policy: default-src 'self'; script-src 'self';`

**4. Firewall / Network Policy Configuration:**
Modify `/home/user/app/network_policy.json`. Change the firewall rule for the `/admin` route to allow connections specifically from the loopback address. Update the action to `ALLOW` and the allowed IP to `127.0.0.1`.

You do not need to start or restart the web server; the automated testing suite will verify your files directly.