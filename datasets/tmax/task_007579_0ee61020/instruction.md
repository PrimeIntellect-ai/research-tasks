You are acting as a compliance analyst for a web company. A recent security incident requires you to generate an automated audit trail. The incident response team has provided you with two files in your home directory (`/home/user`):

1. `web_traffic.log`: A custom-formatted web server log file containing recent HTTP requests.
2. `suspicious_module.so`: An ELF shared object file recovered from the compromised server. The attackers used this module to beacon out to their Command & Control server.

Your task is to:
1. **Analyze the ELF Binary**: Inspect `/home/user/suspicious_module.so` to extract the hardcoded HTTP headers the malware uses for its beacons. You need to find a `User-Agent` string that begins with `X-Compliance-Bot/` and a `Cookie` header that begins with `auth_token_v2=`.
2. **Perform Intrusion Detection**: Write a Python script at `/home/user/generate_audit.py` that parses `web_traffic.log`. The script must identify all requests that contain *both* the exact `User-Agent` and the exact `Cookie` value you extracted from the binary.
3. **Generate the Audit Trail**: Your Python script must output a JSON file at `/home/user/audit_report.json` containing the extracted IOCs (Indicators of Compromise) and a sorted, deduplicated list of malicious IP addresses that made the beaconing requests.

The log file format is:
`IP_ADDRESS | TIMESTAMP | METHOD PATH | STATUS_CODE | USER_AGENT | COOKIE`

The output `/home/user/audit_report.json` must exactly match this schema:
```json
{
  "extracted_iocs": {
    "user_agent": "<exact User-Agent string from binary>",
    "cookie": "<exact Cookie string from binary>"
  },
  "malicious_ips": [
    "<ip1>",
    "<ip2>"
  ]
}
```

Write the Python script, execute it, and ensure the resulting JSON file is perfectly formatted.