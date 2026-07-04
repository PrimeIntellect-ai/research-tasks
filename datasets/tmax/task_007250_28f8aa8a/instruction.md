You are an incident responder investigating a compromised Linux server. We have identified a suspicious executable acting as a sandboxed worker process, located at `/home/user/suspicious_binary`. We suspect this binary contains an embedded TLS certificate used for malicious encrypted communications. 

Your task is to analyze this binary, extract the hidden certificate, and parse its details using Python. 

Please perform the following steps:

1. **File Integrity Verification:** Calculate the SHA256 hash of `/home/user/suspicious_binary`.
2. **ELF/Binary Analysis:** Identify and extract the embedded X.509 certificate (in PEM format) from the binary. The certificate will be stored in plain text within the binary's read-only data section and includes the standard `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` boundaries. Save this extracted certificate exactly as it appears to `/home/user/extracted_cert.pem`.
3. **TLS Certificate Analysis:** Write a Python script that reads `/home/user/extracted_cert.pem` and extracts:
   - The Subject's Common Name (CN).
   - The SHA256 fingerprint of the certificate (as a continuous hex string without colons).
4. **Reporting:** Consolidate your findings by creating a JSON file at `/home/user/cert_info.json` with the following exact structure:

```json
{
  "binary_sha256": "<SHA256 hash of the executable>",
  "cert_cn": "<Extracted Common Name>",
  "cert_fingerprint": "<Extracted Certificate SHA256 Fingerprint>"
}
```

Ensure the Python script successfully executes and generates the correct JSON file. You may use any standard Python libraries or the `cryptography` package (which is available in the environment) to parse the certificate.