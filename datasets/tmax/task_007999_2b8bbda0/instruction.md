You are acting as a DevSecOps engineer. We recently detected anomalous activity in our internal Python web service. We need you to fix a vulnerability in the code, analyze the logs to identify the attackers, and enforce a security policy to block them.

Your task has three phases:

**Phase 1: Vulnerability Analysis and Remediation**
We have a local web service script at `/home/user/app/server.py`. It uses SQLite3 and has an endpoint that is vulnerable to SQL injection.
1. Analyze `/home/user/app/server.py`.
2. Identify the SQL injection vulnerability.
3. Write a patched version of the file to `/home/user/app/server_fixed.py` that uses parameterized queries to prevent the injection. Do not change the behavior of the application for legitimate requests, only fix the vulnerability. 

**Phase 2: Log Parsing and Token Validation**
The service access logs are located at `/home/user/logs/access.log`. The logs contain the IP address, HTTP request, status code, and the JWT token passed in the Authorization header.
1. You must parse this log file to find requests that successfully exploited the SQL injection (i.e., requests that contain SQL syntax like `UNION`, `OR 1=1`, or `--` in the URL parameters AND resulted in a `200` HTTP status code).
2. For each malicious request, extract the JWT token.
3. Validate the JWT token using the public key located at `/home/user/keys/public.pem`. The tokens use the `RS256` algorithm. You may install standard Python packages like `PyJWT` or `cryptography` in the user environment to help with this.
4. Extract the `client_id` claim from the valid, decoded JWTs of the attackers. Ignore any malicious requests where the JWT is invalid or expired.

**Phase 3: Policy Enforcement Generation**
Write a Python script `/home/user/generate_policy.py` that automates Phase 2 and generates a network policy file.
When executed as `python3 /home/user/generate_policy.py`, it must output a JSON file at `/home/user/policy.json` with the following exact structure:
```json
{
  "blocked_entities": [
    {
      "ip": "<attacker_ip>",
      "client_id": "<jwt_client_id>"
    },
    ...
  ]
}
```
Sort the `blocked_entities` list in ascending alphabetical order by the `ip` address. Ensure your script only includes IPs that executed successful SQL injection attacks *and* provided cryptographically valid JWTs.

Complete all three phases to secure the system.