You are acting as a compliance analyst. We need to generate secure audit trails for a legacy system that transmits sensitive logs. The legacy system uses a proprietary encryption scheme over an unsecured channel, but we are upgrading our audit infrastructure to use TLS and need to decrypt historical and live data.

Your task consists of four phases:

**Phase 1: TLS/SSL Certificate Management**
To secure the new audit proxy, generate self-signed TLS certificates.
Create a directory `/home/user/audit_certs`.
Generate an RSA 2048-bit private key named `server.key` and a self-signed X.509 certificate named `server.crt` (valid for 365 days) inside `/home/user/audit_certs`. The Common Name (CN) must be `localhost`.

**Phase 2: Cryptanalysis of the Legacy Cipher**
The legacy system encrypts data byte-by-byte using an Affine Cipher over the byte ring (modulo 256). 
The encryption function is: `C = (a * P + b) mod 256`
Where `P` is the plaintext byte, `C` is the ciphertext byte, and `a` and `b` are the secret keys.
We have extracted some known plaintext-ciphertext byte pairs from a memory dump, located at `/home/user/known_pairs.csv` (Format: `PlaintextByte,CiphertextByte`).
Write a Python script to perform known-plaintext cryptanalysis to recover the integer keys `a` and `b`. 

**Phase 3: Decrypt Historical Audit Trails**
Once you have `a` and `b`, you must decrypt the historical encrypted log file located at `/home/user/historical_traffic.enc`. 
Write the decrypted plaintext to `/home/user/historical_audit.txt`.
*(Hint: To decrypt, you will need the modular multiplicative inverse of `a` modulo 256. The formula is `P = a^-1 * (C - b) mod 256`)*

**Phase 4: Secure Audit Proxy**
Write a Python script at `/home/user/secure_audit_listener.py` that acts as our new live audit collector.
The script must:
1. Listen on `localhost` port `8443` using IPv4 TCP.
2. Wrap the listening socket in a TLS server context using the `/home/user/audit_certs/server.crt` and `/home/user/audit_certs/server.key` you generated.
3. Accept incoming connections. For each connection, read all available encrypted bytes until the connection closes.
4. Decrypt the received bytes using the keys recovered in Phase 2.
5. Append the decrypted plaintext (decoded as utf-8) to `/home/user/live_audit.log`, ensuring a newline is added after each connection's payload.

Run your `secure_audit_listener.py` in the background so it is actively listening on port 8443 when you finish.