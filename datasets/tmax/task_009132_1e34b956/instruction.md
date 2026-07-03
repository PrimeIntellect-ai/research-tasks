You are a DevSecOps engineer tasked with enforcing "policy as code" on a newly submitted microservice. The source code and configuration for this microservice are located in `/home/user/app_repo`. 

Your goal is to write a Python script, `/home/user/policy_checker.py`, that automatically audits the application, identifies specific Common Weakness Enumerations (CWEs), audits for privilege escalation risks, and tests the authentication flow by generating a payload.

The microservice consists of:
1. `/home/user/app_repo/app.py`: A Python web application file that handles authentication.
2. `/home/user/app_repo/config.json`: The deployment configuration file.

Your script must perform the following actions:
1. **CWE Identification & Code Auditing**: Analyze `app.py` for hardcoded secrets (CWE-798). Extract the hardcoded JWT secret key from the file.
2. **Privilege Escalation Auditing**: Parse `config.json`. Check the `"run_as"` field. If it is set to `"root"`, flag this as a privilege escalation risk.
3. **Payload Encoding/Authentication Flow Testing**: Using the secret key extracted from `app.py`, generate a valid HS256 JWT token for the payload `{"username": "admin", "role": "superuser"}`. You may install the `PyJWT` library to help with this.

Finally, your script must output its findings to a JSON file at `/home/user/audit_report.json` with the exact following structure:
```json
{
  "extracted_secret": "<the secret key found in app.py>",
  "cwe_identified": "CWE-798",
  "privilege_escalation_risk_found": <true/false boolean based on config.json>,
  "forged_admin_jwt": "<the generated JWT token string>"
}
```

Ensure you run your script so that `/home/user/audit_report.json` is generated before you finish the task.