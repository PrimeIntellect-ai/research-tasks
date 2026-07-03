You are a DevSecOps engineer tasked with enforcing security policies and recovering a legacy web application deployment bundle. 

The deployment bundle `/home/user/deploy_bundle.enc` is an encrypted gzip tarball (`.tar.gz`). It was encrypted using OpenSSL with the following parameters: `-aes-256-cbc -pbkdf2`. 
The original engineer lost the full passphrase, but remembers it starts with the exact string `Deploy2023_` followed by exactly four digits (e.g., `Deploy2023_0000` to `Deploy2023_9999`).

Perform the following tasks using shell commands or scripts (Python, Bash, etc.):

1. **Password Cracking & Decryption:**
   Write a script to brute-force the passphrase. Decrypt `/home/user/deploy_bundle.enc` to `/home/user/deploy_bundle.tar.gz` and extract its contents to `/home/user/deploy`. 

2. **TLS/SSL Certificate Management:**
   The application requires a new TLS certificate. Generate a self-signed RSA 2048-bit certificate and private key.
   - Output files: `/home/user/deploy/certs/server.crt` and `/home/user/deploy/certs/server.key`
   - Expiration: Exactly 365 days
   - Common Name (CN): `secure.internal.dev`
   - (Leave other Subject fields blank or default).

3. **Content Security Policy (CSP) Enforcement:**
   Inside the extracted bundle, there is an Nginx configuration file at `/home/user/deploy/nginx.conf`. It contains an overly permissive CSP header: 
   `add_header Content-Security-Policy "default-src *";`
   Programmatically modify this file to enforce a strict policy. Replace that exact line with:
   `add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';";`

4. **File Permission & Access Control:**
   The permissions of the extracted files in `/home/user/deploy/app/` are dangerously broad. Fix them using the principle of least privilege:
   - All directories inside `/home/user/deploy/app/` must have octal permissions `0755`.
   - All standard files inside `/home/user/deploy/app/` must have octal permissions `0644`.
   - **Exception:** The sensitive configuration file `/home/user/deploy/app/config.json` must have strict `0400` permissions.

5. **Audit Logging:**
   Create an audit log at `/home/user/audit_log.txt` with exactly four lines containing the following information (and nothing else):
   - Line 1: The discovered passphrase.
   - Line 2: The SHA-256 checksum of the generated `/home/user/deploy/certs/server.crt` (just the hash, no file path).
   - Line 3: The newly inserted CSP line extracted from `nginx.conf` (e.g., `add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';";`).
   - Line 4: The octal permissions of `config.json` (exactly `400` or `0400`).