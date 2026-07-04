You are a DevSecOps engineer building a "policy-as-code" automated vulnerability scanner for your deployment pipeline. 

Your task is to write a Python script at `/home/user/policy_scanner.py` that analyzes a web application's TLS certificate and HTTP headers to ensure they meet strict security standards. 

You have been provided with two artifacts from a simulated staging environment:
1. `/home/user/cert.pem`: The public TLS certificate of the staging server.
2. `/home/user/headers.json`: A JSON file containing a dictionary of HTTP response headers returned by the server.

Your script `/home/user/policy_scanner.py` must take exactly two command-line arguments:
`python3 /home/user/policy_scanner.py <path_to_cert_pem> <path_to_headers_json>`

The script must evaluate the following security rules and write a vulnerability report to `/home/user/scan_report.json`.

### Security Rules
1. **TLS Expiration (Rule ID: `TLS_EXPIRED`)**: The certificate must not be expired. Use the current system time for comparison. If the `Not After` date is in the past, flag this violation.
2. **TLS Weak Signature (Rule ID: `TLS_WEAK_SIG`)**: The certificate must not use weak signature algorithms. Specifically, if the signature algorithm is `sha1WithRSAEncryption` or `md5WithRSAEncryption`, flag this violation. (You may use Python's standard libraries or invoke `openssl` via `subprocess` to parse the certificate).
3. **CSP Missing (Rule ID: `CSP_MISSING`)**: The HTTP headers must contain a `Content-Security-Policy` key. If missing, flag this violation.
4. **CSP Unsafe (Rule ID: `CSP_UNSAFE`)**: If the `Content-Security-Policy` header exists, it must NOT contain the directives `'unsafe-inline'` or `'unsafe-eval'` (case-insensitive check). If it contains either, flag this violation.

### Output Format
Your script must output a strictly formatted JSON file to `/home/user/scan_report.json`. The JSON must contain a single root object with a `violations` key. The value must be a list of the string Rule IDs that were violated, sorted alphabetically.

Example expected format for `/home/user/scan_report.json`:
```json
{
  "violations": [
    "CSP_UNSAFE",
    "TLS_EXPIRED",
    "TLS_WEAK_SIG"
  ]
}
```

If no rules are violated, the `violations` list should be empty `[]`.

Write the script, then execute it against the provided `/home/user/cert.pem` and `/home/user/headers.json` files to generate the final `/home/user/scan_report.json`. Ensure the output file is valid JSON.