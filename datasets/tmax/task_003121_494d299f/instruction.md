You are a DevSecOps engineer performing a security audit and enforcing policy as code. We have a strict policy against passing credentials via command-line arguments because they become visible to all users on the system via process listing tools (e.g., `/proc` or `ps`). 

A recent process execution log snapshot has been saved to `/home/user/logs/process.log`. We suspect one of the Python scripts in the `/home/user/app/` directory violated this policy by accepting a sensitive key as a command-line argument.

Your tasks are:
1. **Log Analysis & CWE Auditing**: Parse `/home/user/logs/process.log` to identify the leaky script and the exact secret key that was exposed.
2. **Code Remediation**: Modify the identified leaky script in `/home/user/app/` so that it no longer accepts the key via a command-line argument. Instead, refactor it to read the key from the `BACKUP_KEY` environment variable. Ensure the script remains functional otherwise.
3. **Decryption**: The leaked key was used to encrypt a sensitive file located at `/home/user/data/secret.enc`. The file was encrypted using standard OpenSSL AES-256-CBC with PBKDF2 (`openssl enc -aes-256-cbc -pbkdf2 -d -in <file> -pass pass:<key>`). Decrypt this file to recover the original secret text.
4. **Hashing & Reporting**: Calculate the SHA256 hash of the decrypted secret text (ensure no trailing newlines are included in the hash calculation). 

Finally, write a report to `/home/user/report.txt` with exactly the following format:
Line 1: The exact filename of the leaky script (e.g., `script.py`)
Line 2: The leaked secret key found in the log
Line 3: The decrypted secret text
Line 4: The SHA-256 hash of the decrypted secret text

Ensure your report is exact and contains no extra text or blank lines.