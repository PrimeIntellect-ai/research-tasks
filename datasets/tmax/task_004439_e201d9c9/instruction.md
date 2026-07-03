You are a network engineer analyzing suspicious HTTP traffic. You have been provided with a log of recent HTTP requests in JSON format at `/home/user/http_traffic.json`. We suspect that an attacker is using an automated vulnerability scanner to probe our web application for Path Traversal (CWE-22) vulnerabilities and attempting Privilege Escalation (CWE-269) by tampering with session cookies.

Your task is to write a Python script at `/home/user/detect_attacks.py` that reads `/home/user/http_traffic.json` and performs pattern matching to identify these attacks.

The JSON file contains a list of objects with the following structure:
```json
[
  {
    "ip": "192.168.1.x",
    "method": "GET",
    "path": "/some/path",
    "headers": {
      "User-Agent": "...",
      "Cookie": "session=..."
    }
  }
]
```

Your script must implement the following inspection rules:
1. **CWE-22 (Path Traversal):** Inspect the `path` field. If the path contains the string `../` (either plain or URL-encoded as `%2E%2E%2F`), flag it as CWE-22.
2. **CWE-269 (Privilege Escalation):** Inspect the `Cookie` header. The `session` cookie value (everything after `session=`) is a Base64-encoded JSON string. Decode it and parse the JSON. If the `role` key is exactly `"admin"` or `"administrator"`, flag it as CWE-269. (Ignore missing or malformed cookies/JSON).

For every flagged request, your script must append a line to `/home/user/alerts.log` in the exact format:
`<IP_ADDRESS> - <CWE_ID>`

Requirements:
- If a single request triggers both rules, output a line for each CWE (CWE-22 first, then CWE-269).
- Ensure the output file `/home/user/alerts.log` is created.
- You must write and execute this script to generate the final log file.