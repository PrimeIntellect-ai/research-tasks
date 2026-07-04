You are a forensics analyst investigating a compromised Linux host. The incident response team has collected evidence from a web server that was recently breached. The attackers leveraged a vulnerability in the login flow to steal an administrator's session token, which they then used as a key to encrypt sensitive system data before exfiltrating it (though we blocked the exfiltration, the data remains encrypted locally).

The evidence is located in `/home/user/evidence/`:
1. `/home/user/evidence/login.py`: The source code of the vulnerable authentication routing module.
2. `/home/user/evidence/app.log`: Application logs from the time of the attack.
3. `/home/user/evidence/stolen_data.enc`: A file containing sensitive data encrypted by the attacker.

Your objectives:
1. **Code Auditing & CWE Identification**: Analyze `login.py` to identify the precise vulnerability that allowed the attacker to steal the token via the login flow. Determine its exact CWE ID (e.g., CWE-123).
2. **Log Parsing & Token Recovery**: Parse `app.log` to find the malicious request where the token was leaked. The token is a Base64-encoded JSON object. Extract it and decode it to recover the attacker's encryption key (stored in the `key` field).
3. **Decryption**: The attacker used the recovered key to encrypt `stolen_data.enc` using the standard Python `cryptography.fernet.Fernet` scheme. Write a Python script to decrypt the file's contents.

Finally, write your findings to `/home/user/forensics_report.txt` in the exact following format:
```
CWE: CWE-XXX
Leaked Token Key: <extracted_key_string>
Decrypted Content: <decrypted_plaintext>
```

Replace `CWE-XXX` with the correct ID for the vulnerability, `<extracted_key_string>` with the extracted Fernet key, and `<decrypted_plaintext>` with the decrypted contents of the file. You may use any Python libraries available or install them via pip if needed.