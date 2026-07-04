You are a compliance analyst investigating a recent security incident. An attacker bypassed our authentication system, exploited an injection vulnerability, and escalated privileges. We need you to perform a forensic analysis and generate an audit trail report. 

You have been provided with the following evidence on the system:
1. **Certificate Chain**: `/home/user/certs/server_chain.pem` - Our load balancer's certificate chain. We suspect one of the intermediate certificates has expired, which prevented our Web Application Firewall (WAF) from inspecting TLS traffic.
2. **API Traffic Logs**: `/home/user/logs/api_traffic.log` - Contains raw HTTP request logs. The attacker bypassed the token verification by sending a JWT that explicitly specifies no signature algorithm.
3. **System Audit Logs**: `/home/user/logs/privilege_events.json` - Contains a chronological list of role changes in the application. The attacker used the bypassed authentication to execute a Cross-Site Scripting (XSS) payload that forced an admin to grant them elevated privileges.

Your task is to analyze these files using Python and bash commands, and create a final audit report.

Create a Python script (or scripts) to perform the following:
1. **Certificate Validation**: Parse `/home/user/certs/server_chain.pem`. Identify the expired certificate in the chain. Extract its Subject Common Name (CN).
2. **Intrusion Detection**: Scan `/home/user/logs/api_traffic.log` to find the HTTP request that contains a JSON Web Token (JWT) in the `Authorization: Bearer <token>` header where the token header specifies `"alg": "none"` (or similar bypass). 
3. **Vulnerability Analysis**: Decode the payload of the compromised JWT found in step 2. Extract the exact malicious XSS string embedded in the token's `profile_data` field. Also, identify the source IP address of this request from the log entry.
4. **Privilege Escalation Auditing**: Examine `/home/user/logs/privilege_events.json`. Find the event where a user was granted the `SuperAdmin` role within 5 minutes (300 seconds) after the timestamp of the malicious API request found in step 2. Identify the `target_user` who received this role.

Finally, you must output your findings to a JSON file located at `/home/user/audit_report.json` with the following exact structure:
```json
{
  "expired_cert_cn": "Common Name of the expired certificate",
  "attacker_ip": "IP address of the attacker",
  "xss_payload": "The exact XSS payload string from the JWT",
  "escalated_user": "The username of the account that received SuperAdmin"
}
```

Ensure all analysis is automated via scripts where possible. Do not modify the original log files.