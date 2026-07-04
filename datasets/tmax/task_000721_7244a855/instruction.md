You are an incident responder investigating a local web application suspected of being compromised. The application is a custom Python Flask employee portal running locally on `http://127.0.0.1:8080`.

You have been assigned three critical remediation tasks:

**Phase 1: Privilege Escalation Auditing & Cryptography Analysis**
The application uses a custom encrypted cookie named `auth_token` for session management. We suspect an attacker might be able to forge this token to escalate their privileges to an administrator if they obtain the encryption key. 
1. Search the application directory (`/home/user/app`) for any leaked secrets or backup files that might expose the encryption key.
2. An access log containing a recently captured standard user token is located at `/home/user/logs/auth.log`. 
3. Analyze the application's source code (`/home/user/app/app.py`) to understand the encryption and decryption routine (AES CBC mode).
4. Using the leaked key, write a Python script to decrypt the captured token, modify the payload to escalate the privileges to the `admin` role, and encrypt the new payload to forge an admin token.
5. Send an HTTP GET request to `http://127.0.0.1:8080/admin_dashboard` using your forged `auth_token` cookie. Save the exact text response (which contains a secret flag) to `/home/user/admin_flag.txt`.

**Phase 2: Content Security Policy (CSP) Enforcement**
During the incident, we also discovered that the application is actively being targeted by Cross-Site Scripting (XSS) attacks. 
1. Modify the Flask application code at `/home/user/app/app.py` to enforce a strict Content Security Policy.
2. You must add an application-wide response header `Content-Security-Policy` with the exact value: `default-src 'self'; script-src 'self'` to all HTTP responses.
3. Restart the Flask application so your changes take effect. The application must continue listening on `127.0.0.1:8080`.

**Constraints and Notes:**
* You may need to install standard cryptographic libraries like `pycryptodome` and `flask` to run the app and write your exploit.
* The application runs in the background. You may kill the existing process and restart it after patching.
* Ensure your forged token correctly handles PKCS7 padding, matching the application's implementation.