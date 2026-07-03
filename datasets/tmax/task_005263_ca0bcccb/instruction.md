You are a network engineer analyzing an intercepted traffic dump. You have extracted several artifacts from the capture, and your goal is to validate the server's identity, secure the recovered credentials, and decrypt the intercepted traffic payload using a combination of shell commands and Python.

You have the following files in `/home/user/`:
- `ca.crt`: The Certificate Authority certificate.
- `server.crt`: The server's certificate extracted from the TLS handshake.
- `ssh_key_b64.txt`: A base64-encoded SSH private key recovered from a compromised configuration payload.
- `sym.key.enc`: A symmetric key encrypted with the SSH RSA public key.
- `traffic.enc`: The intercepted traffic payload, encrypted via AES-256-CBC.
- `iv.bin`: The 16-byte initialization vector used for the AES encryption.

Perform the following tasks:
1. **Certificate Validation**: Verify if `server.crt` is valid and properly signed by `ca.crt`. Write the exact word `VALID` or `INVALID` to `/home/user/cert_status.txt` based on your findings.
2. **SSH Key Management**: Decode the `ssh_key_b64.txt` file and save the private key to `/home/user/.ssh/id_rsa`. You must apply the strict, standard SSH file permissions to this private key so that the SSH client would not reject it.
3. **RSA Decryption**: Use the recovered private key (`id_rsa`) to decrypt `sym.key.enc`. Save the decrypted 32-byte symmetric key to `/home/user/sym.key`. (You may use `openssl` for this).
4. **Traffic Decryption**: Write a Python script at `/home/user/decrypt_traffic.py` that reads the AES-256-CBC key from `sym.key`, the IV from `iv.bin`, and the ciphertext from `traffic.enc`. The script must decrypt the traffic and output the plaintext to `/home/user/decrypted_payload.txt`. Execute your script to produce the output file. You may use the `cryptography` library in Python.

Ensure all requested output files (`cert_status.txt`, `id_rsa`, `sym.key`, `decrypt_traffic.py`, and `decrypted_payload.txt`) are created exactly at the specified paths.