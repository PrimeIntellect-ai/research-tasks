You are an incident responder investigating a recent security breach involving an open redirect vulnerability on a custom C-based authentication service. 

Your investigation involves three phases: vulnerability remediation, log analysis, and certificate inspection. 

**Phase 1: Vulnerability Remediation**
You have been provided the source code of the authentication service's redirect handler at `/home/user/login_service.c`. Currently, it takes a single command-line argument representing the `next` URL parameter and prints a raw HTTP `Location` header. It suffers from an Open Redirect vulnerability because it does not validate the input.
1. Modify `/home/user/login_service.c` to enforce strict validation on the input parameter:
   - The parameter MUST start exactly with the string `/secure/`.
   - The parameter MUST NOT contain the substring `//` (to prevent protocol-relative URL bypasses).
   - If the input is valid, print `Location: <input>\r\n\r\n`.
   - If the input is invalid, fallback to printing `Location: /secure/default\r\n\r\n`.
2. Compile the fixed code to an executable located exactly at `/home/user/login_service`. Ensure it has execute permissions. Use `gcc` to compile it.

**Phase 2: Log Analysis**
The attacker exploited this vulnerability before it was discovered. You have a dump of the authentication logs at `/home/user/auth_logs.txt`. 
1. Parse this log file to identify all unique IP addresses that successfully triggered a redirect (HTTP status `302`) to any URL containing the malicious domain `evil.com`.
2. You may use shell utilities or write a custom script/program to extract this data.

**Phase 3: Certificate Inspection**
The attacker also left behind a suspicious TLS certificate during their lateral movement. The certificate is located at `/home/user/suspicious.crt`.
1. Analyze this X.509 certificate to extract the `Organization Name` (O) field from the certificate's `Issuer` details.

**Final Deliverable**
Compile your findings into a JSON report located at `/home/user/report.json`. The file must exactly match this structure:
```json
{
  "malicious_ips": [
    "ip_address_1",
    "ip_address_2"
  ],
  "issuer_org": "Extracted Organization Name"
}
```
*Note: The `malicious_ips` array must be sorted in alphabetical (lexicographical) order.*