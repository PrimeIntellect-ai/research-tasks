You are a DevSecOps engineer responsible for enforcing security policies on a company's internal authentication portal. The portal currently suffers from an open redirect vulnerability in its login flow and uses weak, default administrator credentials.

The system is deployed under `/app/` and consists of three services:
1. **NGINX** (Reverse Proxy) - Listens on port 8000.
2. **Flask Login Service** - Listens on port 5000.
3. **Redis** - Session store on port 6379.

Your tasks are as follows:

**Phase 1: Privilege Escalation and Authentication Audit**
The current application configuration file located at `/app/auth_config.json` contains the administrator's password hash (MD4/MD5 format).
1. Perform a dictionary attack or brute-force search to crack this weak hash.
2. Save the cracked plaintext password in a file exactly at `/home/user/cracked_password.txt`.
3. Update `/app/auth_config.json` with a new, strong password (at least 16 characters, alphanumeric) replacing the old hash with a securely hashed version (bcrypt) of your new password.

**Phase 2: Open Redirect Remediation (Policy as Code)**
The Flask service uses a `?next=` query parameter during login that blindly redirects users, enabling phishing attacks. You must build a standalone Python-based validator service that NGINX will use to sanitize redirects.
1. Create a Python script at `/home/user/validator.py` that runs an HTTP server on port 8080.
2. The server must expose a `/validate` endpoint. It will receive a `next` query parameter (e.g., `/validate?next=/dashboard`).
3. Your service must act as a strict classifier:
   - If the `next` parameter is a safe, local, relative path (e.g., `/dashboard`, `/profile`), return HTTP 200 OK.
   - If the `next` parameter is malicious or an absolute URL pointing to an external domain (e.g., `http://evil.com`, `//evil.com`, `javascript:alert(1)`), return HTTP 403 Forbidden.
   - We have provided two test corpora at `/app/corpus/clean/` (files containing safe URLs, one per line) and `/app/corpus/evil/` (files containing malicious URLs, one per line) for you to test your logic. 

**Phase 3: Multi-Service Integration**
1. Modify the NGINX configuration at `/app/nginx.conf` to use the `auth_request` module (or similar proxy logic) to intercept requests to the `/login` endpoint. Before NGINX passes the request to the Flask backend, it must forward the `next` parameter to your Python validator on port 8080. If your validator returns 403, NGINX must drop the request and return a 403 status to the client.
2. Ensure all three core services (NGINX, Flask, Redis) and your new `validator.py` service are successfully running and communicating. A startup script at `/app/start_services.sh` is provided, but you must launch your validator separately or append it to the script.

To complete the task, ensure that:
- NGINX routes traffic on port 8000.
- Your Python validator is listening on port 8080 and enforcing the redirect policy.
- `/home/user/cracked_password.txt` contains the correct original plaintext password.