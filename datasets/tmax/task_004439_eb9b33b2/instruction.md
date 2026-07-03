You are an incident responder investigating a recently compromised Linux server. The attacker has altered system configurations, left a backdoor, and encrypted a critical system file. 

Your investigation and remediation must follow these steps:
1. **Service Auditing:** The attacker left a rogue service listening on a TCP port between 8000 and 9000. Identify the port, find the associated process, and terminate it.
2. **Privilege Escalation Auditing:** The attacker created a hidden SUID binary in `/var/tmp/`. Locate it and remove its SUID permission.
3. **SSH Hardening:** The attacker modified `/etc/ssh/sshd_config` to allow root login without passwords. Correct this configuration to secure SSH (set `PermitRootLogin prohibit-password` or `no`).
4. **Decryption Tool Development (C++):** 
   The attacker left an image file at `/app/ransom_note.png` containing the parameters of their custom encryption algorithm. Extract the text from this image (e.g., using `tesseract`). The image describes the *encryption* steps applied to each byte.
   
   You must write a C++ program at `/home/user/decryptor.cpp` and compile it to `/home/user/decryptor`. 
   - The program must read binary ciphertext from `stdin` and output the plaintext to `stdout`.
   - It must implement the exact inverse of the algorithm described in the ransom note to decrypt the data byte-by-byte.
   - For example, if the note says "ENCRYPT: SUB 0x10 THEN XOR 0x20", your decryptor must XOR 0x20 THEN ADD 0x10. (Be careful with 8-bit integer overflows/underflows; all operations should wrap around naturally like an `unsigned char`).

Compile your decryptor executable to `/home/user/decryptor`. An automated verification system will extensively fuzz your `decryptor` binary against a recovered reference oracle with thousands of random byte streams to ensure bit-exact equivalence.