You are a penetration tester reviewing an intercepted backup archive from a compromised jump server. Your workspace is located at `/home/user/workspace`.

Inside this directory, you will find:
1. `secret_backup.zip`: An encrypted ZIP file containing sensitive server configurations and logs.
2. `wordlist.txt`: A list of potential passwords for the ZIP file.

Your objective is to extract the archive, analyze its contents, remediate specific security risks, and generate a final report.

Perform the following steps:

1. **Password Cracking**: Brute-force the password for `secret_backup.zip` using the provided `wordlist.txt` and standard command-line tools. Extract the contents to `/home/user/workspace/extracted/`.
2. **Certificate Validation**: Inside the extracted folder, there is a file named `chain.pem` containing multiple certificates. Use `openssl` to inspect them. Identify the Common Name (CN) of the single certificate in the chain that is *expired*.
3. **Sensitive Data Redaction**: The extracted folder contains `db_backup.log`. This file accidentally leaked AWS-style API keys. Find all instances of strings starting with `AKIA` followed by exactly 16 uppercase letters or digits (e.g., `AKIA1234567890ABCDEF`). Create a new file at `/home/user/workspace/db_backup_redacted.log` where all such keys are replaced with the exact string `[REDACTED]`.
4. **SSH Hardening & File Permissions**: The archive contains an SSH private key `id_rsa` and a configuration file `sshd_config`.
   - Copy `id_rsa` to `/home/user/.ssh/id_rsa` and apply the correct, secure file permissions required by SSH for private keys.
   - Modify the extracted `sshd_config` file directly in the `extracted` directory: locate the directive permitting empty passwords and change it from `yes` to `no` to harden the configuration.

**Reporting:**
Generate a final report at `/home/user/workspace/report.txt` with exactly the following three lines:
Line 1: The cracked password for the zip file.
Line 2: The exact Common Name (CN) of the expired certificate.
Line 3: The SHA256 checksum of your modified `sshd_config` file.