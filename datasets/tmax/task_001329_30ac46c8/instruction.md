You are a security engineer assigned to perform credential rotation and sensitive data cleanup on a web application's server. The application's configuration files are located in the directory `/home/user/app_configs/`. 

Recently, the old database password was leaked, and it was discovered that AWS credentials were inappropriately hardcoded into some configuration files instead of using IAM roles. 

Your task is to secure these configuration files using Bash commands or by writing a Bash script. You must perform the following actions:

1. **Credential Rotation:** 
   Search through all `.conf` files in `/home/user/app_configs/` and replace every instance of the old database password `OldVulnerablePass123` with the new password `NewSecureDBPass2024!`.

2. **Sensitive Data Redaction:** 
   Find any hardcoded AWS keys in the `.conf` files. Replace the values of any line starting with `AWS_ACCESS_KEY_ID=` or `AWS_SECRET_ACCESS_KEY=` with exactly the string `REDACTED`. 
   For example, `AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE` should become `AWS_ACCESS_KEY_ID=REDACTED`.

3. **File Permission and Access Control:** 
   Ensure that all `.conf` files in `/home/user/app_configs/` have strict permissions set to `600` (read and write for the owner only), as they contain sensitive configurations.

4. **Cryptographic Hashing:** 
   After modifying the files and updating permissions, generate a SHA-256 checksum for all `.conf` files in `/home/user/app_configs/`. Process the files in alphabetical order. Save the standard output of the `sha256sum` command directly to `/home/user/configs_checksum.txt`. 

You may use standard Linux utilities (e.g., `sed`, `awk`, `chmod`, `sha256sum`, `find`) to complete this task.