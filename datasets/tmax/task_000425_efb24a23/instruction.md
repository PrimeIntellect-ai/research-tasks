You are a penetration tester analyzing a compromised Linux server. You have discovered a suspicious executable left by an attacker and an encrypted payload. Your objective is to reverse engineer the binary to find a cryptographic key, use it to decrypt the payload, and analyze the resulting TLS certificate.

You must accomplish the following steps using only Bash, coreutils, and standard command-line tools:

1. **Binary Analysis**:
   Analyze the ELF executable located at `/home/user/scanner.elf`. The attacker hid a 1-byte XOR key inside a custom ELF section named `.secret_key`. Extract this single byte (in hexadecimal format).

2. **Cryptanalysis & Decryption**:
   The attacker encrypted a stolen TLS certificate using a simple single-byte XOR cipher with the key you found. The encrypted payload is located at `/home/user/cert.enc`. Decrypt this file and save the decrypted output to `/home/user/decrypted.crt`. The decrypted file should be a valid x509 certificate in PEM format.

3. **Certificate Management & Hashing**:
   Analyze the decrypted certificate (`/home/user/decrypted.crt`) using OpenSSL (which is standard). Extract the following information:
   - The Subject Common Name (CN).
   - The SHA-256 fingerprint of the certificate.

4. **Reporting**:
   Create a report file at `/home/user/report.txt` containing exactly three lines in the following format:
   ```
   KEY: <the 1-byte key in 0xXX format, e.g., 0x5A>
   SUBJECT_CN: <the extracted Common Name>
   FINGERPRINT: <the SHA-256 fingerprint, uppercase, colon-separated>
   ```

Do not install any external tools. Use standard utilities like `readelf`, `objdump`, `openssl`, `awk`, `xxd`, and bash built-ins. Ensure your output file exactly matches the requested format.