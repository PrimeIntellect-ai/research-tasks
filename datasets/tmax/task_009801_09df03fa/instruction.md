You are a forensics analyst investigating a recently compromised Linux host. The attacker exfiltrated data but left behind an encrypted evidence file and a checksum. They used a misconfigured backup process to store their encryption key.

Your objective is to locate the attacker's key, decrypt the evidence, verify its integrity, and extract the hidden flag.

Here is what we know about the system:
1. The attacker encrypted the evidence using Python's `cryptography.fernet.Fernet` module. The encrypted file is located at `/home/user/forensics/evidence.enc`.
2. The attacker stored their base64-encoded Fernet key in a hidden backup file somewhere inside the `/home/user/system_backup/` directory. Due to a privilege misconfiguration, this file was left world-readable.
3. The decrypted evidence will be a JSON-formatted string containing a key called `"secret_evidence"`.
4. A SHA-256 checksum of the *raw value* of `"secret_evidence"` (just the string itself, no newlines or JSON formatting) is stored in `/home/user/forensics/checksum.txt`.

Perform the following steps:
1. Find the hidden, world-readable file containing the Fernet key in `/home/user/system_backup/`.
2. Write a Python script at `/home/user/forensics/recover.py` that:
   - Reads the key.
   - Decrypts `/home/user/forensics/evidence.enc`.
   - Parses the decrypted JSON.
   - Extracts the value associated with `"secret_evidence"`.
   - Computes the SHA-256 hash of the extracted value and asserts that it matches the hash in `/home/user/forensics/checksum.txt`.
   - Writes *only* the extracted `"secret_evidence"` string to `/home/user/forensics/flag.txt`.
3. Run your script to produce `/home/user/forensics/flag.txt`.

Ensure your final output file (`/home/user/forensics/flag.txt`) contains exactly the extracted string without any trailing whitespace or newlines.