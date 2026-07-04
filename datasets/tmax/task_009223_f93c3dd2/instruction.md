You are acting as a compliance analyst. Your organization requires automated audit trails for all web-facing services to ensure file integrity, vulnerability management, and TLS compliance. 

You have been assigned to audit a newly deployed authentication microservice. The source code for the service is located at `/home/user/server.py` and its bundled TLS certificate is located at `/home/user/server.crt`.

We suspect that the login flow in `server.py` contains an Unvalidated Redirects and Forwards vulnerability (also known as an Open Redirect).

Your task is to write a Python script `/home/user/generate_audit.py` and run it to produce a JSON audit report at `/home/user/audit_report.json`.

The `audit_report.json` must strictly follow this format:
```json
{
  "audit_target": "/home/user/server.py",
  "integrity_hash": "<SHA-256 hash of server.py>",
  "vulnerability": {
    "cwe": "CWE-601",
    "parameter_name": "<the name of the vulnerable HTTP GET parameter causing the redirect>",
    "line_number": <integer representing the exact line number in server.py where the redirect function is called with the vulnerable parameter>
  },
  "tls_compliance": {
    "certificate": "/home/user/server.crt",
    "expiration_date": "<Expiration date of the certificate in YYYY-MM-DD format>"
  }
}
```

Constraints and Requirements:
1. You must identify the specific parameter causing the open redirect and the exact line number it is executed on in `/home/user/server.py`.
2. You must compute the SHA-256 hash of `/home/user/server.py` to ensure file integrity.
3. You must extract the `notAfter` (expiration) date from `/home/user/server.crt` and format it as `YYYY-MM-DD`.
4. Run your script to generate the `/home/user/audit_report.json` file.