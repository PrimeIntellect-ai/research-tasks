You are a forensics analyst investigating a compromised Linux host. The attacker used a malicious script that inadvertently leaked stolen authentication tokens via command-line arguments (captured in a process monitor log). They also established an encrypted exfiltration tunnel using a custom TLS client certificate signed by their own rogue Certificate Authority (CA).

You have been provided with an evidence directory at `/home/user/evidence/` containing the following files:
1. `/home/user/evidence/process_list.txt`: A snapshot of running processes captured during the attack. The attacker ran a script named `exfiltrate.sh` which passed the stolen token via the `--auth-token` argument.
2. `/home/user/evidence/web_access.log`: Simulated web server logs that contain requests involving the stolen token in the `Authorization: Bearer` header.
3. `/home/user/evidence/rogue_ca.pem`: The attacker's rogue CA certificate recovered from memory.
4. `/home/user/evidence/certs/`: A directory containing several client certificates (`.pem` format). One of these belongs to the attacker and was signed by the `rogue_ca.pem`. The others are benign and signed by a different CA.

Perform the following tasks:
1. **Intrusion Detection & Pattern Matching:** Analyze `/home/user/evidence/process_list.txt` to identify the leaked authentication token.
2. **Sensitive Data Redaction:** Create a new file at `/home/user/evidence/web_access_redacted.log`. This file must be an exact copy of `web_access.log`, except every occurrence of the leaked token must be replaced with the exact string `[REDACTED]`.
3. **Certificate Chain Validation:** Verify the certificates in `/home/user/evidence/certs/` against `/home/user/evidence/rogue_ca.pem` to identify the specific certificate file that was signed by the rogue CA.
4. **Reporting:** Create a JSON file at `/home/user/report.json` with your findings. It must use the following exact format:
```json
{
  "leaked_token": "THE_EXTRACTED_TOKEN_HERE",
  "malicious_cert_file": "filename.pem"
}
```
*(Note: Use just the filename for `malicious_cert_file`, e.g., `cert_3.pem`, not the full path).*