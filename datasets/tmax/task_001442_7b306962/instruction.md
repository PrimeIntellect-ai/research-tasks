You are a DevSecOps engineer enforcing policy as code. We have a staging API server for an internal application that must be tested for compliance before deployment. 

The API server script is located at `/home/user/server.py`. Your task is to:
1. Start the server in the background. It will run on `http://127.0.0.1:8080`.
2. Write a Python security testing script at `/home/user/policy_tester.py` that performs the following actions:

**Action 1: Authentication Flow Testing & Cookie Inspection**
- Send a `POST` request to `http://127.0.0.1:8080/api/login` with the JSON payload `{"username": "admin", "password": "password123"}`.
- Inspect the `Set-Cookie` header in the response for the `session_id` cookie.
- Determine if the `session_id` cookie possesses the `HttpOnly` and `Secure` attributes.

**Action 2: HTTP Header Inspection**
- Inspect the response headers from the `/api/login` endpoint.
- Compare the returned headers against this list of required security headers: `["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]`.
- Identify exactly which of these required headers are missing from the response.

**Action 3: Sensitive Data Redaction**
- Using the `session_id` cookie obtained from the login, send a `GET` request to `http://127.0.0.1:8080/api/users`.
- The endpoint will return a JSON list of user profiles containing sensitive Social Security Numbers (SSNs) in the format `XXX-XX-XXXX`.
- Parse the JSON response and redact all SSNs by replacing them with the exact string `***-**-****`. Leave all other data intact.

**Action 4: Generate Compliance Report**
- Your script must output the findings to a strictly formatted JSON file at `/home/user/compliance_report.json`.
- The JSON file must have the following exact structure:
```json
{
  "cookie_security": {
    "has_httponly": <boolean>,
    "has_secure": <boolean>
  },
  "missing_security_headers": [
    "<header_name_1>",
    "<header_name_2>"
  ],
  "redacted_users": [
    {
      "name": "<name>",
      "ssn": "***-**-****",
      "role": "<role>"
    }
  ]
}
```
*Note: Sort the `missing_security_headers` array alphabetically.*

Execute your script to produce `/home/user/compliance_report.json`. You may install necessary Python libraries like `requests` using `pip` without root privileges.