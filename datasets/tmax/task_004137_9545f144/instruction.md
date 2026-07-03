You are an incident responder acting as a forensics analyst recovering evidence from a compromised Linux host. The attacker exfiltrated sensitive data, encrypted it, and left a persistence mechanism. 

You have been provided a directory at `/home/user/forensics/` containing the following evidence files:
1. `/home/user/forensics/syslog_dump.txt`: A recent extraction of system logs.
2. `/home/user/forensics/exfiltrated_data.enc`: An encrypted payload containing intercepted network traffic.
3. `/home/user/forensics/authorized_keys`: A copy of the compromised user's SSH `authorized_keys` file.

Your objectives are to:

1. **Log Parsing & Correlation:** Analyze `/home/user/forensics/syslog_dump.txt` to identify the encryption key. The attacker used a malicious process named `exfiltrator` which accidentally logged its AES-256-CBC Key and IV in hexadecimal format.
2. **Decryption:** Use the extracted Key and IV to decrypt `/home/user/forensics/exfiltrated_data.enc`. The file was encrypted using AES-256-CBC.
3. **HTTP Header Inspection:** The decrypted payload contains raw HTTP request logs. Parse the decrypted HTTP data to extract the value of the `X-Stolen-Auth-Token` header.
4. **SSH Key Management:** The attacker added a persistence SSH key to `/home/user/forensics/authorized_keys` with the comment `backdoor@hacker.local`. 
    - Remove this malicious key from the `authorized_keys` file in place.
    - Calculate the SHA256 fingerprint of the *malicious key* you removed (in standard OpenSSH Base64 fingerprint format, e.g., `SHA256:xxxx...`).

5. **Reporting:** Create a JSON report at `/home/user/forensics_report.json` with the exact following schema:
```json
{
  "aes_key": "<extracted_hex_key>",
  "stolen_token": "<extracted_auth_token>",
  "malicious_key_fingerprint": "<malicious_key_sha256_fingerprint>"
}
```

Ensure all file paths used are absolute. You may write auxiliary scripts in Python, Bash, or any other standard utility available on a Linux system to accomplish these tasks.