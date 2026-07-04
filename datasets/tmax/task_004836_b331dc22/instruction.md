You are acting as a penetration tester auditing a simulated local service. Your objective is to extract hidden credentials by performing port scanning, binary analysis, decryption, and password cracking.

The environment contains a simulated service and a compiled daemon binary. Complete the following phases:

**Phase 1: Service Auditing**
1. Start the simulation by running: `python3 /home/user/simulation.py &`
   (Wait a few seconds for it to bind the ports).
2. Write a Python script to scan `localhost` on TCP ports `10000` through `10050`. Most ports will immediately drop your connection. Exactly one port will accept the connection and immediately send you a raw stream of binary data before closing.
3. Capture this binary data and save it. This is your encrypted payload.

**Phase 2: Binary Analysis**
1. Analyze the compiled ELF executable located at `/home/user/auth_daemon`. 
2. This binary contains a hardcoded 16-byte AES key and a 16-byte AES IV stored in its read-only data section. 
3. Locate them. The key is prefixed with the string `KEY_ID=` and the IV is prefixed with `IV_ID=`. Extract the 16 characters following each prefix.

**Phase 3: Decryption**
1. Use the extracted key and IV to decrypt the binary payload you captured in Phase 1. The encryption algorithm used is AES-128-CBC with PKCS7 padding.
2. You may use Python's `cryptography` library for this (`pip install cryptography` if needed).
3. The decrypted payload is a JSON string containing a `salt` value and a dictionary of user `hashes`.

**Phase 4: Password Cracking**
1. The extracted hashes are generated using `SHA256(password + salt)`.
2. The passwords are known to be exactly 4-digit numeric PINs (from `0000` to `9999`).
3. Write a Python brute-force script to crack the passwords for all users in the JSON object.

**Phase 5: Reporting**
Generate a final report at `/home/user/pentest_report.json` containing your findings. The file must strictly match this JSON schema:
```json
{
  "open_port": 10000, 
  "aes_key": "16_byte_key_here",
  "aes_iv": "16_byte_iv__here",
  "cracked_passwords": {
    "user1": "0000",
    "user2": "0000"
  }
}
```
*Note: Replace the values above with your actual findings. The `open_port` must be an integer.*