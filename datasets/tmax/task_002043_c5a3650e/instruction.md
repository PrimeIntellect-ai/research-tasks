You are a security engineer tasked with rotating credentials and hardening our staging web infrastructure. The previous engineer left an infrastructure diagram containing the master decryption password, but unfortunately, only an image of this diagram is available.

Your objectives are to extract the password, unpack the infrastructure configuration, and write a Python script that automates SSH hardening, Content Security Policy (CSP) enforcement, and basic vulnerability log scanning.

Step 1: Information Extraction
An image of the network diagram is located at `/app/diagram.png`. Use OCR (e.g., `tesseract`, which is installed) to extract the master decryption password embedded in the image text.

Step 2: Environment Setup
Use the extracted password to decrypt and extract the archive located at `/home/user/infra.zip` (it is an AES-256 encrypted zip file, decryptable via standard utilities like `7z` or `unzip -P`).
Extract it into `/home/user/infra/`.

Inside, you will find:
- `ssh_config`: The SSH configuration file for the web servers.
- `nginx.conf`: The web server configuration.
- `access.log`: A recent traffic log for the web app.

Step 3: Automation Script
Write a Python script at `/home/user/harden.py` that performs the following operations and run it:

1. **SSH Hardening & Key Management:**
   - Generate a new, passphrase-less Ed25519 SSH keypair saved as `/home/user/infra/id_ed25519` (you can call the `ssh-keygen` command from your script).
   - Modify `/home/user/infra/ssh_config` to ensure:
     - `PasswordAuthentication` is set to `no`.
     - `IdentityFile` points to `/home/user/infra/id_ed25519`.

2. **Content Security Policy Enforcement:**
   - Parse `/home/user/infra/nginx.conf` and inject a strict CSP header into the `server` block.
   - The CSP must include `default-src 'self'`, and it must explicitly prevent both inline scripts and `eval()` execution by omitting `'unsafe-inline'` and `'unsafe-eval'`.

3. **Automated Vulnerability Scanning (Log Analysis):**
   - Parse `/home/user/infra/access.log` to identify all IP addresses that attempted Directory Traversal attacks (look for payloads containing `../` or `%2e%2e%2f` in the request path).
   - Output these malicious IPs, one per line, into a file at `/home/user/infra/banned_ips.txt`.

Ensure your Python script successfully executes and modifies the files in place (or writes the expected output files). An automated scoring system will evaluate your hardened configurations and the accuracy of your vulnerability scanning.