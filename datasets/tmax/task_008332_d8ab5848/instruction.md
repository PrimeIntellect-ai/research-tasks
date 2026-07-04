You are a compliance analyst generating an audit trail for a legacy system. As part of a security audit, you have recovered an encrypted private key and an intercepted HTTP traffic log from an old server. 

Your objective is to demonstrate the vulnerability of the legacy system by cracking the key's passphrase, inspecting the traffic log for sensitive cookies, and generating a structured audit report.

Materials provided (you should assume these exist on the system):
1. `/home/user/audit_materials/legacy_key.pem`: A legacy RSA private key encrypted with a weak passphrase. The compliance documentation notes that the passphrase is exactly 4 digits long (e.g., 0000 to 9999).
2. `/home/user/audit_materials/http_traffic.log`: A text file containing raw HTTP response headers from the legacy application.

Your Tasks:
1. Write a Python script to programmatically brute-force the 4-digit passphrase of `/home/user/audit_materials/legacy_key.pem`. You may use Python libraries like `paramiko` or `cryptography`, or shell out to standard tools like `openssl` within your script.
2. Inspect `/home/user/audit_materials/http_traffic.log` to find the `Set-Cookie` header. Extract the exact value of the `AuditSession` cookie (excluding any flags like Secure or HttpOnly).
3. Generate a JSON formatted audit trail file at `/home/user/audit_report.json` containing the cracked passphrase and the extracted cookie.

The final output file `/home/user/audit_report.json` must exactly match the following format:
```json
{
  "cracked_passphrase": "<the 4-digit PIN>",
  "audit_session_cookie": "<the extracted cookie value>"
}
```

Ensure your JSON file is well-formed. Do not leave any background processes running once you are finished.