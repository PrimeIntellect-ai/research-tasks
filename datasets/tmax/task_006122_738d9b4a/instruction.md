You are an incident responder investigating a compromised internal web application. The application source code and its SQLite database are located in `/home/user/app/`. The attackers managed to steal a highly sensitive system flag, and your goal is to recreate their attack chain to verify the vulnerabilities.

The application is a simple Python Flask web server. Based on initial forensic analysis, the attackers exploited three distinct vulnerabilities to achieve their goal:
1. **Authentication Bypass**: They bypassed the login mechanism without knowing any valid passwords.
2. **Privilege Escalation**: They elevated a standard user account to an administrative role.
3. **Stored XSS Simulation**: They injected a specific Cross-Site Scripting (XSS) payload into their profile, which was then triggered by an automated admin-checking routine to extract the final secret.

Your task:
1. Navigate to `/home/user/app/` and start the Flask application in the background (it runs on `127.0.0.1:5000`).
2. Audit the source code in `/home/user/app/app.py` to identify the three vulnerabilities mentioned above.
3. Write a Python Exploit Proof-of-Concept (PoC) script at `/home/user/poc.py` that automates the attack chain against the local running application.
4. Your PoC must:
   - Exploit the authentication flow to log in as the existing standard user `investigator` (you do not know their password).
   - Exploit the privilege escalation vulnerability to make the `investigator` account an admin.
   - Exploit the profile update endpoint to inject a basic XSS payload (`<script>alert(1)</script>`) into the correct field to satisfy the XSS verification check.
   - Access the `/admin/flag` endpoint using your new admin session to retrieve the secret flag.
5. Save the retrieved flag to a file at `/home/user/flag.txt`.

The automated test will verify the success of your investigation by checking the contents of `/home/user/flag.txt`. Ensure your PoC is robust and successfully executes the entire chain.