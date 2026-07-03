You are an incident responder investigating a recent breach on an internal web service. We suspect an attacker successfully executed remote code on our staging server. 

Your investigation has three phases: Log Correlation, Exploit Replication, and WAF Policy Generation.

**Phase 1: Log Correlation**
You have been provided with an HTTP access log at `/home/user/logs/access.log`. 
1. Analyze the log to identify the attacker's IP address. The attacker made several failed attempts resulting in HTTP 500 errors before finally getting an HTTP 200 OK on a specific API endpoint. They injected their payload using a custom HTTP header.
2. Create a report file at `/home/user/incident_report.json` with the following exact JSON schema:
```json
{
  "attacker_ip": "IP_ADDRESS_HERE",
  "vulnerable_header": "HEADER_NAME_HERE"
}
```

**Phase 2: Exploit Replication**
We have secured a copy of the vulnerable application source code at `/home/user/app/server.py`. The application is currently running locally on port 8080 (`http://localhost:8080`).
1. Review the source code to understand how the custom header is being parsed and processed. (Hint: Look for insecure deserialization).
2. Craft a benign exploit payload using Python to confirm the vulnerability. Your exploit must execute a system command on the vulnerable application to create a file at `/home/user/exploit_success.txt` containing exactly the word `EXPLOITED`.
3. Send your crafted payload to the local application (e.g., via `curl` or a Python script) targeting the vulnerable endpoint and header.

**Phase 3: WAF Policy Configuration**
To prevent this attack from happening in production, we need to generate a configuration file for our Python-based Web Application Firewall (WAF).
1. Create a WAF policy file at `/home/user/waf_rules.json` with the following JSON schema:
```json
{
  "blocked_ips": [
    "ATTACKER_IP_HERE"
  ],
  "blocked_headers": [
    "VULNERABLE_HEADER_HERE"
  ]
}
```

Ensure all paths are strictly adhered to. You may write and execute any intermediate Python scripts needed to parse logs or craft the exploit.