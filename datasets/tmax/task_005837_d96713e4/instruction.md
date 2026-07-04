You are an incident responder investigating a series of suspicious web requests on a Linux server. The attacker left behind an obfuscated Python script used to generate the malicious payloads, and you have the server access logs containing the encoded payloads.

Your task is to:
1. Analyze the obfuscated script located at `/home/user/encoder.py` to reverse engineer the payload encoding/encryption mechanism and extract the secret key.
2. Parse the web server log file located at `/home/user/access.log`. The log contains lines with HTTP GET requests. Extract the encoded payloads from the `payload=` query parameter.
3. Decrypt and decode each payload using the mechanism and key you discovered.
4. Analyze the decrypted payloads to identify the underlying vulnerability type being exploited. You must classify each payload as either a SQL Injection (`CWE-89`) or a Cross-Site Scripting (`CWE-79`) attack.
5. Generate a JSON report of your findings and save it to `/home/user/incident_report.json`.

The JSON report must strictly follow this schema:
```json
[
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "decrypted_payload": "the exact decrypted string",
    "cwe": "CWE-XX"
  },
  ...
]
```
Ensure the items in the JSON array follow the exact order they appear in the `access.log`.

Files provided:
- `/home/user/encoder.py`: The obfuscated payload generator script.
- `/home/user/access.log`: The server log containing the suspicious requests.