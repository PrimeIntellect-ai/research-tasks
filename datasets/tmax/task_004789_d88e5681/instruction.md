You are a security auditor tasked with responding to a suspected breach in a Python Flask web application. The application handles file uploads but is suspected to be vulnerable to a path traversal attack, which an attacker used to overwrite a sensitive file and establish a privilege escalation vector.

Your task is divided into three phases: Log Correlation, Code Remediation, and Network Policy/WAF Implementation.

**Phase 1: Privilege Escalation & Log Correlation**
1. Analyze the web server access logs located at `/home/user/logs/access.log`. Find the IP address of the attacker who successfully exploited the file upload endpoint (they will have sent a POST request to `/upload` with a path traversal payload that resulted in a HTTP 200 response).
2. Based on the payload used by the attacker, determine which file outside the intended `/home/user/app/uploads/` directory was compromised (overwritten).
3. Create a JSON report at `/home/user/audit_report.json` with the following exact keys:
   - `"attacker_ip"`: The IP address of the attacker.
   - `"compromised_file"`: The absolute path of the file the attacker overwrote.

**Phase 2: Vulnerability Remediation**
The vulnerable application code is located at `/home/user/app/server.py`. 
Modify `/home/user/app/server.py` to fix the path traversal vulnerability in the `/upload` endpoint. Ensure that the uploaded file is strictly saved inside `/home/user/app/uploads/` and that any directory traversal attempts (like using `../`, `..`, or absolute paths starting with `/`) in the uploaded filename are neutralized or rejected. 

**Phase 3: Network Policy (Application-Layer WAF)**
Because you do not have root access to configure `iptables`, you must implement an application-layer firewall policy.
Update `/home/user/app/server.py` to include a `@app.before_request` hook that acts as a simple WAF. It must:
1. Return a `403 Forbidden` response (with the text `"Blocked IP"`) if the incoming request originates from the `"attacker_ip"` identified in Phase 1.
2. Return a `403 Forbidden` response (with the text `"Blocked Traversal"`) if the request URL path contains the literal string `../`.

*Constraints & Information:*
- You do not need root access for this task. All files are owned by `user`.
- The application uses Python 3 and Flask. 
- You can install Flask (`pip install flask`) if you need to run and test the application locally.
- Do not change the existing functional endpoints' names or return formats, except to secure them.