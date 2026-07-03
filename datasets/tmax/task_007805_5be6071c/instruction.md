You are a compliance analyst responsible for generating security audit trails for a multi-language web application. You have been provided with a set of configuration and source files in the `/home/user/audit_data/` directory.

Your task is to analyze these files and generate an automated audit report in JSON format at `/home/user/audit_report.json`.

The `/home/user/audit_data/` directory contains:
1. `nginx.conf` - The web server configuration file.
2. `auth.js` - A Node.js snippet used for session token generation.
3. `cert.pem` - The public SSL/TLS certificate for the application.

You must perform the following compliance checks and populate the JSON report with the exact keys specified:

1. **Content Security Policy (CSP)**
   Examine `nginx.conf`. Determine if the `Content-Security-Policy` header contains either the `unsafe-inline` or `unsafe-eval` directives.
   - Key: `"csp_unsafe"`
   - Value: Boolean (`true` if either unsafe directive is present, `false` otherwise).

2. **Token Generation Vulnerability (CWE Identification)**
   Examine `auth.js`. The token generation mechanism is vulnerable because it uses a cryptographically weak pseudo-random number generator. Identify the specific, most precise CWE identifier for this exact vulnerability (Use of Cryptographically Weak Pseudo-Random Number Generator).
   - Key: `"weak_token_cwe"`
   - Value: String (The CWE identifier, e.g., `"CWE-XXX"`).

3. **TLS/SSL Certificate Management**
   Examine `cert.pem`. Extract the Common Name (CN) from the certificate's Subject field.
   - Key: `"cert_subject_cn"`
   - Value: String (The exact Common Name).

**Expected Output Format (`/home/user/audit_report.json`):**
```json
{
  "csp_unsafe": true,
  "weak_token_cwe": "CWE-XXX",
  "cert_subject_cn": "example.com"
}
```

Ensure your output is strictly valid JSON. Do not include any additional keys.