You are a forensics analyst responding to a compromised web application. The application consists of a Flask frontend and a Python-based authentication backend. 

The application files, logs, and a suspicious payload left by the attacker are located in `/app/`.

Your task consists of two parts: Forensics and Remediation.

**Part 1: Forensics**
1. **Log Analysis:** Parse the web server logs located at `/app/access.log`. The attacker exploited an open redirect vulnerability in the `/login` endpoint (using the `next` parameter) to redirect users to a malicious site, and subsequently uploaded a payload. Identify the IP address of the attacker. The attacker's IP will be the one that successfully triggered the open redirect (HTTP 302 to an external URL starting with `http://` or `https://`) immediately before accessing the `/upload` endpoint.
2. **Binary Analysis:** The attacker dropped an ELF executable at `/app/suspicious_bin`. Analyze this ELF binary to extract the hardcoded secret key. The key is a 32-character alphanumeric string prefixed with `KEY-` located in the `.rodata` section.
3. Write your findings to `/home/user/forensics_report.json` exactly in this format:
```json
{
  "attacker_ip": "<extracted_ip>",
  "extracted_key": "<extracted_key>"
}
```

**Part 2: Remediation & Service Composition**
1. **Fix the Vulnerability:** Modify the Flask application at `/app/frontend.py`. The `/login` route blindly redirects to the URL provided in the `next` query parameter. Secure this by implementing input validation: if the `next` parameter is provided, it must be a relative URL (it must start with a single `/` and must NOT start with `//`). If the validation fails, return an HTTP 400 Bad Request. If valid, redirect to it. If not provided, redirect to `/home`.
2. **Start the Services:** The application requires both the frontend and the auth backend to run. A script is provided at `/app/start.sh` which launches both services (Frontend on port 8080, Backend on port 8081). Once you have fixed the code, execute `/app/start.sh` in the background so the services are running and listening.

Ensure your Python code modifications in `/app/frontend.py` are syntactically correct and properly import any required modules.