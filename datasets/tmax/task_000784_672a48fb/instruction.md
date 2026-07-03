You are acting as a compliance analyst. You need to prepare an internal network audit trail for external auditors. The raw logs contain sensitive payment information, are symmetrically encrypted to prevent tampering, and must be cryptographically associated with the server's TLS certificate issuer for verification.

You have been provided with the following files in your home directory (`/home/user/`):
1. `audit_logs.enc`: A file containing the audit trail. The contents are a JSON string that has been encrypted using the Fernet symmetric encryption algorithm.
2. `secret.key`: A text file containing the base64-encoded Fernet key required to decrypt the logs.
3. `server.crt`: The server's PEM-formatted X.509 TLS certificate.

Write and execute a Python script (e.g., `/home/user/process_audit.py`) to perform the following steps:
1. **Decrypt**: Read and decrypt the contents of `/home/user/audit_logs.enc` using the key in `/home/user/secret.key`. The decrypted plaintext is a JSON-encoded list of dictionaries.
2. **Decode**: Parse the decrypted JSON payload into Python objects.
3. **Certificate Inspection**: Extract the Issuer's Common Name (CN) from `/home/user/server.crt`. You may use Python's `cryptography` library or call out to `openssl` via the `subprocess` module.
4. **Redaction**: Iterate through the parsed log objects. In the `message` field of each log, redact any 16-digit credit card numbers. Credit card numbers may appear in the format `XXXX-XXXX-XXXX-XXXX` or as a contiguous 16-digit string `XXXXXXXXXXXXXXXX`. Replace any match with the exact string `[REDACTED]`.
5. **Enrichment**: Add a new key-value pair to each log dictionary: `"cert_issuer"` set to the extracted Issuer Common Name (e.g., `"ComplianceCA"`).
6. **Output**: Save the cleaned, enriched list of dictionaries as a JSON file at `/home/user/clean_audit.json`. The JSON should be pretty-printed with a 2-space indent.

Ensure your script runs successfully and generates the correct output file.