You are a forensics analyst recovering evidence from a compromised Linux host. The attacker managed to inject a malicious domain into the application's Content Security Policy (CSP) to exfiltrate sensitive data. They also dropped several certificates on the system for a man-in-the-middle SSL bumping attack.

Your task is to write a Python script at `/home/user/recover_evidence.py` that processes the evidence and generates a forensic report. 

The evidence is located in:
- A log file at `/home/user/evidence/server.log`
- A directory of certificates at `/home/user/evidence/certs/`

Your Python script must perform the following steps:
1. **CSP Analysis**: Parse `/home/user/evidence/server.log`. The log contains lines with HTTP headers and payloads. Identify the `Content-Security-Policy` headers. The legitimate policy only contains `default-src 'self';`. Find the malicious domain that was injected into the CSP `report-uri` directive.
2. **Certificate Identification & Hashing**: Scan the PEM-encoded X.509 certificates in `/home/user/evidence/certs/`. Identify the certificate whose Common Name (CN) matches the malicious domain found in the CSP header. Compute the SHA-256 fingerprint of this certificate (the hash of its DER-encoded representation).
3. **Data Redaction**: For the log entry immediately following the malicious CSP header line, extract the JSON payload. This payload contains exfiltrated data, including credit card numbers. Redact any 16-digit credit card number (either contiguous like `1234567812345678` or separated by dashes like `1234-5678-1234-5678`) by replacing the entire matched string with `[REDACTED]`.
4. **Report Generation**: Output the findings to a file at `/home/user/report.txt` in exactly the following format:

```text
Rogue Domain: <malicious_domain>
Rogue Cert Hash: <sha256_hex_digest>
Redacted Payload: <redacted_json_string>
```

Constraints:
- Use standard Python libraries (e.g., `re`, `hashlib`, `ssl`, `cryptography` if installed, or invoke OpenSSL via `subprocess`).
- The log file lines follow this pattern:
  `[INFO] Header: Content-Security-Policy: <policy>`
  `[INFO] Payload: <json_data>`
- You must run your script to generate `/home/user/report.txt` before finishing the task.