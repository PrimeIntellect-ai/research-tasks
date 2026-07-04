You are a compliance analyst tasked with generating a secure audit trail of potential privilege escalation vectors on a Linux system, and making this trail available securely for a remote auditor.

Your task consists of three phases: building a secure auditing tool in C, executing the audit, and securely serving the results over TLS.

**Phase 1: Build the Auditing Tool (`secure_audit.c`)**
Write a C program named `/home/user/secure_audit.c` and compile it to `/home/user/secure_audit`. 
The program must:
1. Accept a single directory path as a command-line argument.
2. Recursively scan the specified directory for regular files that have the `setuid` bit set (a common privilege escalation vector).
3. Collect the absolute paths of all discovered `setuid` files, sorted alphabetically, each followed by a newline character (`\n`).
4. Generate a random 256-bit (32-byte) key and a random 128-bit (16-byte) IV for AES-256-CBC encryption.
5. Encrypt the collected list of file paths using AES-256-CBC via the OpenSSL EVP API. 
6. Write the raw encrypted binary bytes to `/home/user/audit_trail.enc`.
7. Write the generated Key and IV in hexadecimal format to `/home/user/audit_key.txt`. The format must be exactly:
   ```
   KEY: <64 hex characters>
   IV: <32 hex characters>
   ```

*(Note: Assume `gcc` and `libssl-dev` are available on the system. Compile using `-lssl -lcrypto`.)*

**Phase 2: Execute the Audit**
Run your compiled `secure_audit` program against the `/usr/bin` directory. This will produce `/home/user/audit_trail.enc` and `/home/user/audit_key.txt`.

**Phase 3: Secure Delivery (TLS/SSL)**
The remote auditor requires the encrypted audit trail to be served over HTTPS.
1. Create a directory `/home/user/certs/`.
2. Generate a self-signed RSA-2048 TLS/SSL certificate (`audit_cert.pem`) and corresponding unencrypted private key (`audit_key.pem`) in the `certs` directory. Set the Common Name (CN) to `localhost`.
3. Start a simple TLS web server in the background on port `8443` that serves the `/home/user` directory. You must use `openssl s_server` for this. The command should look something like:
   `openssl s_server -key /home/user/certs/audit_key.pem -cert /home/user/certs/audit_cert.pem -accept 8443 -WWW &`

Ensure the server remains running in the background. Do not submit until the server is listening and the encrypted files are in place.