You are a DevSecOps engineer enforcing policy-as-code in a CI/CD pipeline. Your system receives release bundles that must be automatically validated before deployment.

A release bundle is located at `/home/user/release_bundle/`. It contains three files:
1. `requirements.txt`: Python dependencies.
2. `traffic.log`: A sample of recent traffic logs.
3. `server.crt` and `ca.crt`: The server certificate and the Certificate Authority chain.

Write a Python script at `/home/user/policy_check.py` that analyzes this bundle and produces a JSON report at `/home/user/policy_report.json`.

Your script must perform the following checks:
1. **Automated Vulnerability Scanning**: Read `requirements.txt`. Check if the package `requests` is present with a version strictly less than `2.31.0` (which contains a known vulnerability). 
2. **Intrusion Detection**: Read `traffic.log`. Check if any line matches the following regular expression exactly (case-insensitive): `(UNION.*SELECT|OR\s+'1'='1'|\/etc\/passwd)`
3. **Certificate Validation**: Verify that `server.crt` was validly issued by `ca.crt`. You may use the `subprocess` module to call `openssl verify` or use the Python `cryptography` library.

The output at `/home/user/policy_report.json` must be a valid JSON object with exactly these keys (boolean values):
```json
{
  "vulnerable_dependency_found": true/false,
  "intrusion_detected": true/false,
  "certificate_valid": true/false
}
```

Constraints:
- "vulnerable_dependency_found" is `true` if `requests` is found with a version < 2.31.0 (e.g., `requests==2.30.0`), otherwise `false`. Assume standard `==` version pinning in the file.
- "intrusion_detected" is `true` if the regex finds a match in the log file, otherwise `false`.
- "certificate_valid" is `true` if the certificate chain validates successfully, otherwise `false`.

Execute your script so the JSON file is generated.