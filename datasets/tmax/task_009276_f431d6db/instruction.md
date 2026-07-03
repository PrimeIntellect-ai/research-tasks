You are an incident responder investigating a potential breach on a custom web server. The attacker may have tampered with the access logs and swapped out the server's TLS certificate. 

Your task is to perform the following steps:

1. **Reverse Engineering:** You have been provided with a compiled Python byte-code file at `/home/user/auth_handler.pyc`. This file handles authentication logging. Disassemble or reverse engineer this file to recover the hardcoded `SECRET_SALT` used to sign log entries.
2. **Log Integrity and Hashing:** Inspect the log file at `/home/user/access.log`. Every line in this file follows the format:
   `[timestamp] IP: <ip_address> - <request> | <sha256_hash>`
   The `<sha256_hash>` is the SHA-256 digest of the string formed by concatenating the exact log content (everything before the ` | ` separator) and the `SECRET_SALT`.
   Identify the **single** log entry that has been tampered with (where the hash does not match the content + salt).
3. **TLS Certificate Analysis:** Analyze the suspicious certificate left by the attacker at `/home/user/cert.pem`. Extract its SHA-256 fingerprint.

Once you have completed your investigation, create a JSON report at `/home/user/report.json` with the following structure:
```json
{
  "tampered_line_number": <integer_line_number_starting_at_1>,
  "tampered_ip": "<ip_address_from_tampered_line>",
  "cert_fingerprint": "<sha256_fingerprint_of_cert_with_colons>"
}
```

Make sure your fingerprint is formatted with uppercase hex digits and colons (e.g., `A1:B2:C3:...`).