You are a security engineer tasked with rotating the compromised credentials of a legacy internal web server. 

An incident occurred yesterday where an attacker triggered a credential rotation endpoint. You need to investigate the logs, recover the old compromised key from a poorly encrypted backup, verify its integrity, and generate a new set of credentials to complete the rotation safely.

Here are your detailed instructions:

Phase 1: Security Log Parsing
Analyze the web server log located at `/home/user/access.log`. Find the IP address of the user who successfully made a `POST` request to the `/rotate_trigger` endpoint. Note this IP address for your final report.

Phase 2: Cryptanalysis & Recovery
The old TLS private key was backed up to `/home/user/old_credentials.enc`. The previous administrator used a custom C program to encrypt it, whose source is available at `/home/user/legacy_crypto.c`. 
By analyzing `legacy_crypto.c`, you will see it uses a repeating multi-byte XOR cipher. Since you know the backup is a standard unencrypted PEM file (which always starts with `-----BEGIN `), you must mount a known-plaintext attack.
Write a C program at `/home/user/decrypt.c`, compile it, and use it to decrypt `/home/user/old_credentials.enc` to a plaintext file named `/home/user/old_credentials.pem`.

Phase 3: File Integrity Verification
A checksum file is located at `/home/user/checksums.txt`. Verify that your decrypted `/home/user/old_credentials.pem` matches the SHA256 hash provided in that file. If it does not, your decryption was incorrect.

Phase 4: TLS Certificate Management (Rotation)
Now that the old key is recovered and verified, generate a new RSA 2048-bit private key (without a passphrase) saved to `/home/user/new_credentials.pem`. Using this new key, generate a self-signed X.509 certificate saved to `/home/user/new_cert.pem`. The certificate must be valid for 365 days and have the Common Name (CN) `rotated.local`. 

Phase 5: Reporting
Create a final log file at `/home/user/rotation_summary.txt` with exactly the following format:
```
Trigger IP: <IP address from Phase 1>
Old Key Checksum: <SHA256 hash of old_credentials.pem>
New Cert CN: <The Common Name of the newly generated cert>
```

Ensure all generated files remain in `/home/user/` and have the exact names specified.