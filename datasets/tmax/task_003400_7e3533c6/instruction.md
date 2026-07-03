You are a security auditor tasked with performing a local security assessment and remediation in the `/home/user/audit` directory. Please perform the following actions:

1. **File Integrity Verification**: 
   A set of logs is located in `/home/user/audit/logs/`. Their expected SHA256 hashes are listed in `/home/user/audit/checksums.sha256`. Verify the integrity of all files listed in the checksum file. Write the exact base filenames (e.g., `log1.txt`) of any files that fail the integrity check to `/home/user/audit/compromised.txt`, one per line, sorted alphabetically.

2. **TLS/SSL Certificate Management**:
   Generate a new self-signed RSA 2048-bit TLS certificate for the domain `vulnerable.local`. The certificate must be valid for 30 days. Save the private key to `/home/user/audit/key.pem` and the certificate to `/home/user/audit/cert.pem`. Do not encrypt the private key (no passphrase).

3. **Vulnerability Analysis & Payload Delivery**:
   Scan the `/home/user/audit/scripts/` directory to identify any script that has insecure world-writable permissions (i.e., writeable by 'others'). Once identified, append a bash payload to the end of this vulnerable script. The payload must execute `echo "EXPLOITED" > /home/user/audit/pwned.txt` whenever the script is executed. Do not modify the permissions of the script or overwrite its original contents.

Ensure all outputs strictly follow the requested file paths and formats.