You are an incident responder investigating a compromised web application. The attacker managed to execute code and left behind a suspicious script and an encrypted file containing exfiltrated web access logs. 

Your objective is to reverse engineer the attacker's script, recover the password, decrypt the logs, and identify the attacker's IP address based on their intrusion attempts.

All files are located in `/home/user/investigation/`. 

Here is what you know:
1. The attacker dropped an obfuscated Python script at `/home/user/investigation/dropper.py`.
2. This script contains logic for encrypting/decrypting the exfiltrated data, as well as the hash of the password used.
3. The encrypted log file is located at `/home/user/investigation/exfiltrated.dat`.
4. The password used for encryption is exactly 4 lowercase English letters (e.g., 'abcd').
5. Once you decrypt the log file, you need to analyze the HTTP requests. Look for an intrusion attempt that tries to escape a Python sandbox using Server-Side Template Injection (SSTI). The payload will contain the string `__subclasses__`.

Perform the following tasks:
1. Analyze `dropper.py` to understand the encryption mechanism and find the password hash.
2. Brute-force the 4-letter lowercase password.
3. Decrypt `exfiltrated.dat` to recover the original web access log.
4. Parse the decrypted log to find the IP address of the attacker who sent the SSTI sandbox escape payload.
5. Create a report file at `/home/user/investigation/report.txt` with exactly the following format:

```text
Password: [Cracked 4-letter password]
Attacker IP: [IP address]
```

Replace `[Cracked 4-letter password]` and `[IP address]` with your findings. Ensure the format matches exactly.