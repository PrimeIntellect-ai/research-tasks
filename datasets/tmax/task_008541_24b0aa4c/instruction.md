You are a compliance analyst tasked with generating an audit trail for a recent security incident and verifying the security posture of an internal authentication service.

Your workspace is located at `/home/user/workspace`. Inside, you will find two directories: `logs/` and `auth_service/` (these will be present when you start).

Your task consists of three main phases:

**Phase 1: Security Log Parsing and Correlation**
You have two log files:
1. `/home/user/workspace/logs/access.log`: An Nginx-style access log.
2. `/home/user/workspace/logs/auth.json`: Application-level authentication logs in JSON format.

You must correlate these logs to identify a brute-force attacker. Find the single IP address that meets ALL of the following conditions:
- Has strictly more than 3 failed login attempts (HTTP 401 in `access.log`).
- These failures must have corresponding `{"status": "failed"}` entries in `auth.json` originating from the exact same IP and within the same second.
- All these correlated failures must occur within a single 60-second window.

**Phase 2: Authentication Flow Testing & Header Inspection**
There is a local Flask authentication service at `/home/user/workspace/auth_service/app.py`. 
1. Start this service in the background (it binds to `127.0.0.1:5000`). You may need to install standard dependencies like `flask` or `gunicorn`.
2. Write a Python script to authenticate against the `http://127.0.0.1:5000/login` endpoint. Send a POST request with the JSON payload: `{"username": "auditor", "password": "compliance_password"}`.
3. Inspect the response headers and cookies. Check if the `session_token` cookie is protected with the `Secure` and `HttpOnly` attributes.
4. Extract the `audit_receipt` value from the JSON response body.

**Phase 3: Generate Compliance Report**
Create a final JSON report at `/home/user/workspace/compliance_report.json` with the following exact schema:

```json
{
  "brute_force_ip": "1.2.3.4",
  "cookie_secure_flag": true,
  "cookie_httponly_flag": true,
  "audit_receipt": "string_value"
}
```

*Note: Replace the values with your actual findings. The boolean fields should reflect whether the respective flags were present (`true`) or missing (`false`) on the `session_token` cookie.*