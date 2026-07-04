You are a compliance analyst tasked with generating an audit trail for a legacy internal service to demonstrate its severe security flaws. The service is running locally at `https://127.0.0.1:8443`. 

Your objective is to write and execute a Python script that interacts with this service, extracts sensitive data, decrypts it, inspects its TLS certificate, and produces a formatted audit report.

Perform the following steps:
1. **Payload Delivery**: Send a POST request to `https://127.0.0.1:8443/auth` with the form data `username=auditor` and `payload=admin_bypass`. 
2. **TLS Inspection**: Programmatically connect to the server and extract the Common Name (CN) from the Subject of its SSL/TLS certificate.
3. **Cookie Inspection**: Extract the `legacy_session` cookie from the HTTP response of your POST request. This cookie's value is a hex-encoded string.
4. **Decryption**: The cookie is encrypted using AES-128 in ECB mode. The 16-byte encryption key is stored in plain text in `/home/user/app_config/secrets.txt`. Read this key, decode the hex cookie, and decrypt it. (Assume the plaintext uses standard PKCS#7 padding, which you should remove).
5. **Audit Trail Generation**: Output your findings to exactly `/home/user/audit_report.json`. The file must contain valid JSON with the following exact structure:
```json
{
  "cert_cn": "<extracted_common_name>",
  "decrypted_cookie": "<decrypted_plaintext_string>"
}
```

Notes:
- The server uses a self-signed certificate, so you will need to bypass SSL verification for the HTTP request, but you must still extract the certificate details to get the CN.
- You can use standard Python libraries or widely available ones like `requests` and `cryptography` (you may need to install them via `pip`).
- Make sure the resulting JSON file contains the correct, unpadded decrypted string and the exact Common Name from the certificate.