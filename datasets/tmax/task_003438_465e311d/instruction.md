You are a compliance analyst tasked with generating a formal audit trail from a compromised internal web server. A previous incident responder collected a set of artifacts and placed them in `/home/user/evidence/`. You must analyze these artifacts, extract specific security indicators, and produce an immutable audit report.

The `/home/user/evidence/` directory contains:
1. `http_traffic.log`: A raw HTTP traffic log containing recent requests. One of these requests contains a classic SQL injection attempt in the body.
2. `shadow.bak`: A backup of the server's `/etc/shadow` file. The `admin` account is suspected of using a weak password.
3. `server.pem`: The server's public X.509 certificate.
4. `wordlist.txt`: A small dictionary of common passwords used by the organization.

Your task:
Write a script (preferably Python, though you may use bash utilities) to perform the following analysis:
1. **Injection & Cookie Analysis**: Inspect `http_traffic.log` to find the HTTP request containing the string `' OR 1=1` (the SQL injection payload). Extract the value of the `session_id` cookie from that specific request.
2. **Password Cracking**: Crack the password hash for the `admin` user found in `shadow.bak` using the words provided in `wordlist.txt`.
3. **Certificate Inspection**: Extract the Issuer Common Name (CN) from `server.pem`.

Once you have gathered this information, generate an audit report at `/home/user/audit_report.json` with the exact following JSON structure:
```json
{
  "sqli_session_cookie": "extracted_cookie_value_here",
  "admin_password": "cracked_password_here",
  "cert_issuer_cn": "extracted_issuer_cn_here"
}
```

Finally, to comply with evidence protection standards, you must set the file permissions of `/home/user/audit_report.json` to strictly read-only for the owner, and no permissions for anyone else (0400).