You are a security auditor assigned to review a Python-based microservice for a client. The service handles sensitive data and uses JSON Web Tokens (JWT) for authentication. The source code and logs are located in `/home/user/api/`. 

Your objectives are:

1. **Vulnerability Analysis:** Review `/home/user/api/app.py`. Identify the specific Common Weakness Enumeration (CWE) identifier that describes the critical cryptographic vulnerability present in the custom JWT validation logic.
2. **Exploitation:** Write a Python script to exploit this vulnerability. You must forge a JWT to authenticate as the `admin` user and send a GET request to `http://127.0.0.1:8080/admin/data`. Extract the secret key from the JSON response.
3. **Log Analysis & Intrusion Detection:** The file `/home/user/api/server.log` contains HTTP access logs. Write a Python script using regex/pattern matching to inspect the `Authorization` headers in the logs. Identify all unique IP addresses that have attempted to exploit this specific JWT vulnerability (i.e., submitted a token attempting to bypass the signature check using the same technique you used).
4. **Remediation:** Create a patched version of the application code and save it to `/home/user/api/fixed_app.py`. The patched version must securely validate the token, explicitly enforcing the `HS256` algorithm and rejecting unauthenticated or unsigned tokens.

Before starting, install the requirements from `/home/user/api/requirements.txt` and start the server by running `/home/user/start_server.sh`.

Finally, compile your findings into a JSON report located at `/home/user/audit_report.json`. The file must exactly match this structure:
```json
{
  "cwe_id": "CWE-XXX",
  "admin_secret": "the_secret_string_retrieved_from_the_endpoint",
  "malicious_ips": ["1.2.3.4", "5.6.7.8"]
}
```
(Replace "CWE-XXX" with the exact CWE ID, e.g., "CWE-347", sort the IP addresses in ascending order, and insert the retrieved secret).