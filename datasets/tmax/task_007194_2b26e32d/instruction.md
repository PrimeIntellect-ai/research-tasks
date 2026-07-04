You are an incident responder investigating a compromised Linux server. An attacker exploited a path traversal vulnerability in a file upload handler to exfiltrate sensitive data. We managed to recover the attacker's encryption script and the exfiltrated file, but the encryption key was not saved.

Here is what we know:
1. The attacker's script is located at `/home/user/investigation/encryptor.py`.
2. The encrypted and encoded exfiltrated data is at `/home/user/investigation/exfil_data.enc`.
3. The original plaintext file's SHA-256 hash was logged by our file integrity monitoring system and is saved at `/home/user/investigation/original_hash.txt`.
4. Based on command-line logs, we know the attacker provided exactly a 2-byte encryption key to the script.

Your objectives:
1. Analyze `encryptor.py` to understand the payload encoding and encryption routine.
2. Write a Python script to brute-force the 2-byte key.
3. Verify the integrity of your decrypted payload by checking it against the SHA-256 hash in `original_hash.txt`.
4. Once successfully recovered, save the exact original plaintext to `/home/user/investigation/recovered_data.txt`.
5. Write the 2-byte encryption key in uppercase hexadecimal format (e.g., `A1B2`) to `/home/user/investigation/key.log`.