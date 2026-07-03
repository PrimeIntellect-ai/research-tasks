You are a penetration tester performing a local audit of a web server application deployed in the `/home/user/audit_target` directory. You suspect the application has been tampered with, possesses insecure file permissions that could lead to privilege escalation, has invalid SSL configurations, and contains an open redirect vulnerability.

Your task is to write a Python script at `/home/user/auditor.py` that programmatically analyzes the files in `/home/user/audit_target/` and generates an audit report at `/home/user/audit_report.json`.

The `/home/user/audit_target/` directory contains:
1. `login.py` - The main authentication routing script.
2. `checksum.sha256` - A text file containing the expected SHA-256 hash of `login.py` (format: `<hash>  login.py`).
3. `server.crt` - The PEM-encoded SSL certificate used by the web server.

Your Python script (`/home/user/auditor.py`) must do the following when executed:
1. **File Permission Audit**: Check if `/home/user/audit_target/login.py` is world-writable (which would be a local privilege escalation vector if run by a higher-privileged user). 
2. **Cryptographic Checksum Verification**: Compute the SHA-256 hash of the current `login.py` and compare it against the hash provided in `checksum.sha256`. 
3. **Certificate Validation**: Read `server.crt` and determine if the certificate is currently expired.
4. **Vulnerability Analysis (Open Redirect)**: Analyze the contents of `login.py` to find an open redirect vulnerability in the login flow. Specifically, identify the exact HTTP request argument (URL parameter) that is passed directly to the `redirect()` function without sanitization.

Finally, your script must output a JSON file at `/home/user/audit_report.json` with the exact following structure and keys:
```json
{
  "world_writable": <boolean>,
  "checksum_match": <boolean>,
  "cert_expired": <boolean>,
  "open_redirect_param": "<string_name_of_the_parameter>"
}
```

Ensure your script handles everything programmatically and relies on the standard libraries (like `os`, `hashlib`, `json`, `ssl`, `cryptography` or by invoking shell tools like `openssl` via `subprocess`). Do not hardcode the answers; the script must derive them by analyzing the actual files. Run your script to generate the final JSON report.