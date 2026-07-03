You are acting as a penetration tester and security auditor. You have been given access to a simulated environment where a scheduled backup script is allegedly leaking sensitive information, leading to potential local privilege escalation or data breaches.

Your task consists of four phases: Auditing, Exploitation, Decryption, and Remediation.

**Phase 1: Code Auditing**
Review the script located at `/home/user/vulnerable_backup.sh`. This script is used by the system administrators to encrypt sensitive files. 
1. Identify the specific vulnerability that allows local users to view the encryption password.
2. Determine the most appropriate CWE (Common Weakness Enumeration) identifier for "Invocation of Process Using Visible Sensitive Information" (sometimes also related to exposure of credentials).
3. Write the exact CWE ID (e.g., `CWE-123`) into a file named `/home/user/cwe.txt`.

**Phase 2: Exploitation**
The system administrators run this script periodically via a cron-like mechanism. 
1. Execute the simulation by running `/home/user/start_simulation.sh &` in the background. This will repeatedly execute the vulnerable backup script with a secret password.
2. Using only standard bash commands, coreutils, and `/proc` (or `ps`), monitor the system to capture the secret password being used by the `openssl` command.

**Phase 3: Decryption**
You have obtained an encrypted file from the server at `/home/user/secret_data.enc`.
1. Using the password you captured in Phase 2, decrypt `/home/user/secret_data.enc`. The file was encrypted using `aes-256-cbc` with pbkdf2.
2. Save the decrypted contents to `/home/user/decrypted_secret.txt`.

**Phase 4: Remediation (Secure Coding)**
1. Create a patched version of the backup script at `/home/user/secure_backup.sh`.
2. The script must take exactly two arguments: an input file and an output file.
3. It must use `openssl enc -aes-256-cbc -pbkdf2` to encrypt the input file to the output file.
4. Instead of passing the password via a command-line argument (which exposes it to `/proc`), the script must read the password securely from the `BACKUP_PASS` environment variable (using OpenSSL's `env:` pass format or standard input).
5. Ensure `/home/user/secure_backup.sh` has executable permissions.

Complete all phases. An automated test will verify the contents of `/home/user/cwe.txt`, `/home/user/decrypted_secret.txt`, and the security of `/home/user/secure_backup.sh`.